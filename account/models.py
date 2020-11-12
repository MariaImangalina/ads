from django.db import models
from django.contrib import auth
from django.db.models.signals import post_save
from django.dispatch import receiver

from datetime import timedelta, date

User = auth.get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    expiration_date = models.DateField(default=0)

    def __str__(self):
        return self.user.username

    def activated(self):
        if self.expiration_date >= date.today():
            self.is_active = True
        else:
            self.is_active = False
        self.save()
        

    def prolong(self, add_months):
        add_time = timedelta(days=31)*add_months
        if self.expiration_date:
            self.expiration_date += add_time
        else:
            self.expiration_date = date.today() + add_time
        self.save()

