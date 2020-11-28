from django.db import models

from django.contrib.auth import get_user_model

import numpy as np

User = get_user_model()

class Polygon(models.Model):

    ADS_TYPE = [
        ('Сдам', 'Сдам'),
        ('Продам', 'Продам'),
    ]

    name = models.CharField(max_length=250)
    user = models.ForeignKey(User, related_name='polygon', on_delete=models.CASCADE)
    coordinates = models.CharField(max_length=1500)
    ads_type = models.CharField(max_length=150, choices=ADS_TYPE, blank=True, null=True, verbose_name='Тип объявлений')
    min_area = models.PositiveIntegerField(blank=True, null=True, default=0)
    max_area = models.PositiveIntegerField(blank=True, null=True, default=10000000)

    def __str__(self):
        return self.name

        

#square
#type_ads