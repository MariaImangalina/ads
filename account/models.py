from django.db import models
from django.contrib import auth

from datetime import timedelta, date

class User(auth.models.User, auth.models.PermissionsMixin):
    is_active = models.BooleanField(default=False, verbose_name='status'),
    expiration_date = models.DateField(default=0)

    def __str__(self):
        return self.username


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


