from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages
from django.views import generic
from django.db.models import Q
from django.core.mail import EmailMessage

from .forms import PolygonForm, SearchPolygon, PolygonImportForm
from .models import Polygon

from ads.secret import db_user, db_password

import json
import psycopg2
import pandas as pd
from datetime import datetime, timedelta


User=get_user_model()

#######____РАБОЧИЕ ФУНКЦИИ, НЕ VIEWS_______

#_______преобразуем координаты из Array в формат запроса SQL______
def array_to_sql(coordinates):
    cor = [i.strip('),').replace(', ', ' ').strip() for i in coordinates.split('LatLng(')[1:]]
    cor1 = [i.split(' ') for i in (cor + [cor[0]])]
    for i in cor1:
        i.reverse()
    cor2 = [' '.join(i) for i in cor1]
    cor3 = ','.join(cor2)
    return cor3


#_______преобразуем координаты из json в формат запроса SQL______
def json_to_sql(data):
    x = data['features'][0]['geometry']['coordinates'][0]
    x_list = []
    for j in range(len(x)):
        x_element = [str(i) for i in x[j]]
        x_list += [','.join(x_element)]

    x2_list = [i.replace(',', ' ') for i in x_list]
    x3_list = ','.join(x2_list)
    return x3_list

#_______преобразуем координаты из БД для импорта в json__________
def coordinates_to_json(coordinates):
    new = []
    for i in coordinates.split(','):
        new.append(i.split(' '))
    return new



#______запрос к базе данных с объявлениями_________________________
def request_to_db(pol, time):
    ip = '89.223.122.104'
    if time == 'now':
        period = (datetime.now() - timedelta(days=31)).strftime("%Y-%m-%d %H:%M:%S")
    elif time == 'every_hour':
        period = (datetime.now() - timedelta(minutes=90)).strftime("%Y-%m-%d %H:%M:%S")
    else:
        print('Error! Wrong argument. Must be now or every_hour')
    params = ['POLYGON(({}))'.format(pol.coordinates), period, pol.min_area, pol.max_area, ]
    sql = '''
            SELECT *
            FROM ads
            WHERE ST_Contains(ST_GeomFromText(%s,4326),geom) AND time_ads>%s AND square BETWEEN %s and %s
            '''
    if pol.ads_type:
        sql += 'AND type_ads = %s LIMIT 50;'
        params += [pol.ads_type, ]
    else:
        sql += ' LIMIT 50;'
    
    with psycopg2.connect (database="avito", user=db_user, password=db_password, host = ip) as conn:
        with conn.cursor() as curs:
            curs.execute (sql, params)
            records = curs.fetchall()  
            col_names = [desc[0] for desc in curs.description]
            
        df = pd.DataFrame (records, columns = col_names)
    return df


#######__________VIEWS________________

@login_required
def add_polygon(request):
    form = PolygonForm()

    if request.is_ajax and request.method == 'POST':
        formset = PolygonForm(request.POST)

        if formset.is_valid():
            polygon = formset.save(commit=False)
            polygon.user = request.user
            polygon.coordinates = array_to_sql(formset.cleaned_data['coordinates'])
            polygon.save()
            
        else:
            print(formset.errors)

    return render(request, 'data/map.html', {'form':form})


@login_required
def import_polygon(request):
    form = PolygonImportForm()

    if request.method == 'POST' and 'coord_file' in request.FILES:
        file_form = PolygonImportForm(request.POST, request.FILES)
        if file_form.is_valid():
            polygon = file_form.save(commit=False)
            polygon.user = request.user

            json_data = json.load(request.FILES['coord_file'])
            polygon.coordinates = json_to_sql(json_data)

            polygon.save()
            messages.info(request, 'Полигон сохранен')
        else:
            print(file_form.errors)

    return render(request, 'data/polygon_import.html', {'form':form})



@login_required
def export_polygon_to_json(request, pk):
    pol = Polygon.objects.get(pk=pk)
    coordinates = coordinates_to_json(pol.coordinates)
    description = 'Помещения площадью {}-{}м2'.format(pol.min_area, pol.max_area)

    if pol.ads_type == 'Сдам':
        description + ', тип - аренда'
    elif pol.ads_type == 'Продам':
        description + ', тип - продажа'

    dict_data = {'type': 'FeatureCollection',
                'metadata': {'name': pol.name,
                'creator': 'Yandex Map Constructor',
                'description': description},
                'features': [{'type': 'Feature',
                'id': 0,
                'geometry': {'type': 'Polygon',
                    'coordinates': [coordinates]},
                'properties': {'fill': '#ed4543',
                    'fill-opacity': 0.6,
                    'stroke': '#ed4543',
                    'stroke-width': '5',
                    'stroke-opacity': 0.9}}]}

    response = HttpResponse(json.dumps(dict_data), content_type = 'application/json')
    response['Content-Disposition'] = 'attachment; filename="json_{}.geojson"'.format(pol.name)

    return response


#______________отправка объявлений за месяц с кнопки (для тестирования, УДАЛИТЬ)______________

@login_required
def get_df(request):
    for pol in Polygon.objects.filter(user__profile__paid=True):
        df = request_to_db(pol, 'now')

        date = datetime.today().strftime("%Y-%m-%d-%H.%M.%S")
        df.to_excel(f'media/xlsx/ads_for_{pol.name}_{date}.xlsx', index=False)
        
        msg = EmailMessage(f'Объявления на полигоне {pol.name}', 'что-то', '', [pol.user.email, 'varenik_geo@mail.ru'])
        msg.content_subtype = "html"
        msg.attach_file(f'media/xlsx/ads_for_{pol.name}_{date}.xlsx')
        msg.send(fail_silently=False)

    return HttpResponse('its working')





class DeletePolygon(LoginRequiredMixin, generic.DeleteView):
    model = Polygon

    def get_success_url(self):  #поскольку объект удаляется, просто success_url недостаточно, не остается данных по нему
        return reverse_lazy('account:userpage', kwargs={'pk': self.object.user.pk}) 


class UpdatePolygon(LoginRequiredMixin, generic.UpdateView, generic.detail.SingleObjectMixin):
    template_name = 'data/polygon_update.html'
    model = Polygon
    fields = ['name', 'ads_type', 'min_area', 'max_area']
    
    def get_success_url(self): 
        return reverse_lazy('account:userpage', kwargs={'pk': self.object.user.pk})



#_______________поиск среди полигонов____________

class SearchView(generic.ListView):
    model = Polygon
    template_name = 'data/search_results.html'

    def get_queryset(self):
        self.user = self.request.user
        query = self.request.GET.get('q')

        return Polygon.objects.filter(Q(name__icontains=query), user=self.user)



#_______________запрос на разовую выгрузку_____________

from .tasks import get_df_now_task

@login_required
def get_df_celery(request, pk):
    if request.user.profile.paid:
        get_df_now_task.delay(pk)
        messages.info(request, 'Выгрузка отправлена на ваш email')
    else:
        messages.warning(request, 'Для получения выгрузки нужен оплаченный аккаунт')

    return redirect('account:userpage', pk=request.user.pk)