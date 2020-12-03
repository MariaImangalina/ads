from celery import shared_task

from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.contrib import messages

import os
import datetime
import psycopg2
import pandas as pd

from ads.secret import db_user, db_password
from ads.settings import MEDIA_DIR
from .models import Polygon
from .views import request_to_db

User = get_user_model()

@shared_task 
def get_df():
    for pol in Polygon.objects.filter(user__profile__paid=True):
        df = request_to_db(pol, 'every_hour')
        date = datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")
        df.to_excel(f'media/xlsx/ads_for_{pol.name}_{date}.xlsx', index=False)
    
        msg = EmailMessage(f'Объявления на полигоне {pol.name}', 'что-то', '', [pol.user.email, 'varenik_geo@mail.ru'])
        msg.content_subtype = "html"
        msg.attach_file(f'media/xlsx/ads_for_{pol.name}_{date}.xlsx')
        msg.send(fail_silently=False)



@shared_task 
def check_payment():
    for user in User.objects.all():
        user.profile.check_paid()



def clean_media():
    DIR = os.path.join(MEDIA_DIR, 'xlsx')
    for the_file in os.listdir(DIR):
        file_path = os.path.join(DIR, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


@shared_task 
def get_df_now_task(pk):
    pol = Polygon.objects.get(pk=pk)
    df = request_to_db(pol, 'now')

    date = datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")
    df.to_excel(f'media/xlsx/ads_for_{pol.name}_{date}.xlsx', index=False)
    
    msg = EmailMessage(f'Объявления на полигоне {pol.name}', 'что-то', '', [pol.user.email, 'varenik_geo@mail.ru'])
    msg.content_subtype = "html"
    msg.attach_file(f'media/xlsx/ads_for_{pol.name}_{date}.xlsx')
    msg.send(fail_silently=False)
