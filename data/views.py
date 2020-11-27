from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.views import generic
from django.db.models import Q


from .forms import PolygonForm, SearchPolygon
from .models import Polygon
from ads.secret import db_user, db_password


import psycopg2
import pandas as pd
from datetime import datetime, timedelta
from django.core.mail import EmailMessage


User=get_user_model()

### преобразуем координаты из Array в формат запроса SQL
def to_sql(coordinates):
    cor = [i.strip('),').replace(', ', ' ').strip() for i in coordinates.split('LatLng(')[1:]]
    cor1 = [i.split(' ') for i in (cor + [cor[0]])]
    for i in cor1:
        i.reverse()
    cor2 = [' '.join(i) for i in cor1]
    cor3 = ','.join(cor2)
    return cor3


@login_required
def add_polygon(request):
    form = PolygonForm()

    if request.is_ajax and request.method == 'POST':
        formset = PolygonForm(request.POST)
        print('works here')

        if formset.is_valid():
            polygon = formset.save(commit=False)
            polygon.user = request.user
            polygon.coordinates = to_sql(formset.cleaned_data['coordinates'])
            polygon.save()
            print('works!')
        else:
            print(formset.errors)

    return render(request, 'data/map.html', {'form':form})



@login_required
def get_df(request):
    ip = '89.223.122.104'
    for pol in Polygon.objects.filter(user__is_active=True):
        coord = pol.coordinates
        sql = '''
                SELECT *
                FROM ads
                WHERE ST_Contains(ST_GeomFromText(%s,4326),geom)
                LIMIT 100;
                '''
        params = ['POLYGON(({}))'.format(coord), ]
        with psycopg2.connect (database="avito", user=db_user, password=db_password, host = ip) as conn:
            with conn.cursor() as curs:
                curs.execute (sql, params)
                records = curs.fetchall()  
                col_names = [desc[0] for desc in curs.description]

            df = pd.DataFrame (records, columns = col_names)
            date = datetime.today().strftime("%Y-%m-%d-%H.%M.%S")
            df.to_excel(f'media/xlsx/ads_{date}.xlsx', index=False)
            
            msg = EmailMessage(f'Объявления на полигоне {pol.name}', 'что-то', '', [pol.user.email, 'varenik_geo@mail.ru'])
            msg.content_subtype = "html"
            msg.attach_file(f'media/xlsx/ads_{date}.xlsx')
            msg.send(fail_silently=False)

    return HttpResponse('its working')


    #_______________запрос на разовую выгрузку_____________



@login_required
def get_df_now(request, pk):
    ip = '89.223.122.104'
    pol = Polygon.objects.get(pk=pk)
    coord = pol.coordinates
    date = (datetime.now() - timedelta(days=31)).strftime("%Y-%m-%d %H:%M:%S")
    sql = '''
            SELECT *
            FROM ads
            WHERE ST_Contains(ST_GeomFromText(%s,4326),geom) AND time_ads>%s
            LIMIT 100;
            '''
    params = ['POLYGON(({}))'.format(coord), date]
    with psycopg2.connect (database="avito", user=db_user, password=db_password, host = ip) as conn:
        with conn.cursor() as curs:
            curs.execute (sql, params)
            records = curs.fetchall()  
            col_names = [desc[0] for desc in curs.description]
            
        df = pd.DataFrame (records, columns = col_names)
        date = datetime.today().strftime("%Y-%m-%d-%H.%M.%S")
        df.to_excel(f'media/xlsx/ads_{date}.xlsx', index=False)
        
        msg = EmailMessage(f'Объявления на полигоне {pol.name}', 'что-то', '', [pol.user.email, 'varenik_geo@mail.ru'])
        msg.content_subtype = "html"
        msg.attach_file(f'media/xlsx/ads_{date}.xlsx')
        msg.send(fail_silently=False)

        

    return redirect('account:userpage', pk=request.user.pk)



class DeletePolygon(LoginRequiredMixin, generic.DeleteView):
    model = Polygon

    def get_success_url(self):  #поскольку объект удаляется, просто success_url недостаточно, нет данных по нему
        return reverse_lazy('account:userpage', kwargs={'pk': self.object.user.pk}) 


  

class UpdatePolygon(generic.UpdateView, generic.detail.SingleObjectMixin):
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


