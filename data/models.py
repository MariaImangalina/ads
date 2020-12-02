from django.db import models

from django.contrib.auth import get_user_model

import numpy as np

User = get_user_model()

class Polygon(models.Model):

    ADS_TYPE = [
        ('Сдам', 'Сдам'),
        ('Продам', 'Продам'),
    ]

    name = models.CharField(max_length=250, verbose_name='Название полигона')
    user = models.ForeignKey(User, related_name='polygon', on_delete=models.CASCADE)
    coordinates = models.CharField(max_length=8000)
    ads_type = models.CharField(max_length=150, choices=ADS_TYPE, blank=True, null=True, verbose_name='Тип объявлений')
    min_area = models.PositiveIntegerField(blank=True, null=True, default=0, verbose_name='Минимальная площадь, м2')
    max_area = models.PositiveIntegerField(blank=True, null=True, default=10000000, verbose_name='Максимальная площадь, м2')

    def __str__(self):
        return self.name

        

#square
#type_ads