from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView

from cities.models import City
from routes.forms import RouteForm, RouteModelForm
from routes.models import Route
from routes.utils import get_routes
from trains.models import Train


# @login_required
def home(request):
    form = RouteForm()
    context = {
        'form': form,
    }
    return render(request, 'routes/home.html', context=context)


def find_routes(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)

        if form.is_valid():
            try:
                context = get_routes(request, form)
            except ValueError as error:
                messages.error(request, error)
                return render(request, 'routes/home.html', {'form': form})
            return render(request, 'routes/home.html', context=context)

        return render(request, 'routes/home.html', {'form': form})
    else:
        form = RouteForm()
        messages.error(request, 'Нет данных для поиска')

    return render(request, 'routes/home.html', {'form': form})


def add_route(request):
    if request.method == 'POST':
        context = {}
        data = request.POST

        if data:
            total_time = int(data['total_time'])
            from_city_id = int(data['from_city'])
            to_city_id = int(data['to_city'])
            trains = data['trains'].split(',')
            trains_list = [int(train) for train in trains if train.isdigit()]
            trains_select = Train.objects.filter(id__in=trains_list).select_related('from_city', 'to_city')
            cities_select = City.objects.filter(id__in=[from_city_id, to_city_id]).in_bulk()

            form = RouteModelForm(initial={
                'from_city': cities_select[from_city_id],
                'to_city': cities_select[to_city_id],
                'travel_times': total_time,
                'trains': trains_select,
            })

            context['form'] = form

        return render(request, 'routes/route_create.html', context=context)
    else:
        messages.error(request, 'Невозможно сохранить несуществующий маршрут.')
        return redirect('/')


def save_route(request):
    if request.method == 'POST':
        form = RouteModelForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Маршрут успешно сохранен.')
            return redirect('/')

        return render(request, 'routes/route_create.html', {'form': form})
    else:
        messages.error(request, 'Невозможно сохранить несуществующий маршрут.')
        return redirect('/')


class RouteListView(ListView):
    paginate_by = 5
    model = Route
    template_name = 'routes/route_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        form = RouteForm()
        context['form'] = form
        context['title'] = 'Travel - Маршруты'
        return context


class RouteDetailView(DetailView):
    queryset = Route.objects.all()
    template_name = 'routes/route_detail.html'


class RouteDeleteView(LoginRequiredMixin, DeleteView):
    model = Route
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Маршрут успешно удален.')
        return self.post(request, *args, **kwargs)
