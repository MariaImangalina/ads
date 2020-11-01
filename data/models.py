from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

class Polygon(models.Model):
    name = models.CharField(max_length=250, blank=True),
    user = models.ForeignKey(User, related_name='polygon', on_delete=models.CASCADE),
    coordinates = models.CharField(max_length=1500)

    def __str__(self):
        return self.name