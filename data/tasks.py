from celery import shared_task
from django.core.mail import EmailMessage
import datetime
from django.contrib.auth import get_user_model

import psycopg2
import pandas as pd
from ads.secret import db_user, db_password

from .models import Polygon

User = get_user_model()

@shared_task 
def get_df():
    ip = '89.223.122.104'
    for pol in Polygon.objects.filter(user__profile__paid=True):
        coord = pol.coordinates
        with psycopg2.connect (database="avito", user=db_user, password=db_password, host = ip) as conn:
            with conn.cursor() as curs:
                curs.execute ('''
                SELECT *
                FROM ads
                WHERE ST_Contains(ST_GeomFromText('POLYGON(({}))',4326),geom)
                LIMIT 100;
                '''.format(coord))
                records = curs.fetchall()  
                col_names = [desc[0] for desc in curs.description]
            df = pd.DataFrame (records, columns = col_names)
            date = datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")
            df.to_excel(f'media/xlsx/ads_{date}.xlsx', index=False)
        
            msg = EmailMessage(f'Объявления на полигоне {pol.name}', 'что-то', '', [pol.user.email, 'varenik_geo@mail.ru'])
            msg.content_subtype = "html"
            msg.attach_file(f'media/xlsx/ads_{date}.xlsx')
            msg.send(fail_silently=False)


@shared_task 
def check_payment():
    for user in User.objects.all():
        user.profile.check_paid()