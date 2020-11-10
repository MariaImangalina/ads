from celery import shared_task 

import psycopg2
import pandas as pd
from ads.secret import db_user, db_password

from .models import Polygon


def get_df():
    ip = '89.223.122.104'
    for i in Polygon.objects.all(user.is_active == True):
        coord = i.coordinates
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




@shared_task 
def work():
    print('its workin')

