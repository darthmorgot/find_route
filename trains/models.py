from django.core.exceptions import ValidationError
from django.db import models

from cities.models import City


class Train(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Номер поезда')
    travel_time = models.PositiveSmallIntegerField(verbose_name='Время в пути')
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='from_city_set',
                                  verbose_name='Пункт отправления')
    to_city = models.ForeignKey('cities.City', on_delete=models.CASCADE, related_name='to_city_set',
                                verbose_name='Пункт назначения')

    class Meta:
        verbose_name = 'Поезд'
        verbose_name_plural = 'Поезда'
        ordering = ['travel_time']

    def __str__(self):
        return f'Поезд №{self.name}, маршрут следования {self.from_city} - {self.to_city}'

    def clean(self):
        if self.from_city == self.to_city:
            raise ValidationError('Изменить пункт назначения')

        train = Train.objects.filter(from_city=self.from_city, to_city=self.to_city,
                                     travel_time=self.travel_time).exclude(pk=self.pk)

        if train.exists():
            raise ValidationError('Измените время в пути')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
