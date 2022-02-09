from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from cities.models import City
from routes.forms import RouteForm
from trains.models import Train
from routes import views as routes_view
from cities import views as cities_view
from trains import views as trains_view
from routes.utils import dfs_paths, get_graph


class AllTestsCase(TestCase):
    def setUp(self) -> None:
        self.city_A = City.objects.create(name='A')
        self.city_B = City.objects.create(name='B')
        self.city_C = City.objects.create(name='C')
        self.city_D = City.objects.create(name='D')
        self.city_E = City.objects.create(name='E')

        lst = [
            Train(name='t1', from_city=self.city_A, to_city=self.city_B, travel_time=9),
            Train(name='t2', from_city=self.city_B, to_city=self.city_D, travel_time=9),
            Train(name='t3', from_city=self.city_A, to_city=self.city_C, travel_time=9),
            Train(name='t4', from_city=self.city_C, to_city=self.city_B, travel_time=9),
            Train(name='t5', from_city=self.city_B, to_city=self.city_E, travel_time=9),
            Train(name='t6', from_city=self.city_B, to_city=self.city_A, travel_time=9),
            Train(name='t7', from_city=self.city_A, to_city=self.city_C, travel_time=9),
            Train(name='t8', from_city=self.city_E, to_city=self.city_D, travel_time=9),
            Train(name='t9', from_city=self.city_D, to_city=self.city_E, travel_time=9)
        ]

        Train.objects.bulk_create(lst)

    def test_model_city_duplicate(self):
        """
        Тестирование на возникновение ошибки при дублировании города
        """
        city = City(name='A')

        with self.assertRaises(ValidationError):
            city.full_clean()

    def test_model_train_duplicate(self):
        """
        Тестирование на возникновение ошибки при дублировании поезда
        """
        train = Train(name='t1', from_city=self.city_A, to_city=self.city_B, travel_time=119)

        with self.assertRaises(ValidationError):
            train.full_clean()

    def test_model_train_train_duplicate(self):
        """
        Тестирование на возникновение ошибки при дублировании поезда
        """
        train = Train(name='t112', from_city=self.city_A, to_city=self.city_B, travel_time=9)

        with self.assertRaises(ValidationError):
            train.full_clean()

        try:
            train.full_clean()
        except ValidationError as error:
            # self.assertEqual({'__all__': ['Измените время в пути']}, error.message_dict)
            self.assertIn('Измените время в пути', error.messages)

    def test_home_routes_views(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name='routes/home.html')
        self.assertEqual(response.resolver_match.func, routes_view.home)

    def test_cbv_detail_views(self):
        """
        Тестирование правильности вызова конкретного класса
        """
        response = self.client.get(reverse('cities:detail', kwargs={'pk': self.city_A.pk}))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name='cities/city_detail.html')
        self.assertEqual(response.resolver_match.func.__name__, cities_view.CityDetailView.as_view().__name__)

    def test_home_trains_views(self):
        response = self.client.get(reverse('trains:home'))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name='trains/home.html')
        self.assertEqual(response.resolver_match.func.__name__, trains_view.TrainListView.as_view().__name__)

    def test_find_all_routes(self):
        """
        Тестирование графа (нахождения всех маршрутов)
        """
        trains = Train.objects.all()
        graph = get_graph(trains)
        all_routes = list(dfs_paths(graph, self.city_A.pk, self.city_E.pk))

        self.assertEqual(len(all_routes), 4)

    def test_valid_route_form(self):
        data = {
            'from_city': self.city_A.pk,
            'to_city': self.city_E.pk,
            'transit_cities': [self.city_B.pk, self.city_D.pk],
            'travelling_time': 9,
        }
        form = RouteForm(data=data)

        self.assertTrue(form.is_valid())

    def test_invalid_route_form(self):
        data = {
            'from_city': self.city_A.pk,
            'to_city': self.city_E.pk,
            'transit_cities': [self.city_B.pk, self.city_D.pk],
        }
        form = RouteForm(data=data)

        data = {
            'from_city': self.city_A.pk,
            'to_city': self.city_E.pk,
            'transit_cities': [self.city_B.pk, self.city_D.pk],
            'travelling_time': 9.8485,
        }
        form = RouteForm(data=data)

        self.assertFalse(form.is_valid())

    def test_message_error_more_way_time(self):
        data = {
            'from_city': self.city_A.pk,
            'to_city': self.city_E.pk,
            'transit_cities': [self.city_C.pk],
            'travelling_time': 9,
        }
        response = self.client.post('/find_routes/', data)

        self.assertContains(response, 'Время в пути больше заданного.', 1, 200)

    def test_message_error_from_cities(self):
        data = {
            'from_city': self.city_B.pk,
            'to_city': self.city_E.pk,
            'transit_cities': [self.city_C.pk],
            'travelling_time': 945,
        }
        response = self.client.post('/find_routes/', data)

        self.assertContains(response, 'Маршрут через указанные города невозможен.', 1, 200)
