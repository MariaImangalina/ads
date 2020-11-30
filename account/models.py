from django.db import models
from django.contrib import auth
from django.db.models.signals import post_save
from django.dispatch import receiver

from datetime import timedelta, date

User = auth.get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    expiration_date = models.DateField(default=(date.today()-timedelta(days=1))) #ПОПРАВИТЬ
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def check_paid(self):
        if self.expiration_date >= date.today():
            self.paid = True
        else:
            self.paid = False
        self.save()



        
#возможно, понадобится потом для расширения админки
def prolong(self, add_months):
    add_time = timedelta(days=31)*add_months
    if self.expiration_date:
        self.expiration_date += add_time
    else:
        self.expiration_date = date.today() + add_time
    self.save()

