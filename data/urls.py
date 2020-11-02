from django.urls import path, include

from .views import add_polygon


app_name = 'data'

urlpatterns = [
    path('map/', add_polygon, name='add_polygon'),
]
