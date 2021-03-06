from django.urls import path, include

from .views import add_polygon, get_df, DeletePolygon, SearchView, UpdatePolygon, import_polygon, get_df_celery, export_polygon_to_json

app_name = 'data'

urlpatterns = [
    path('map/', add_polygon, name='map'),
    path('df/', get_df, name='df'),
    path('remove/<int:pk>/', DeletePolygon.as_view(), name='remove'),
    path('search/', SearchView.as_view(), name='search'),
    path('update/<int:pk>/', UpdatePolygon.as_view(), name='update'),
    path('get_now/<int:pk>/', get_df_celery, name='get_df_now'),
    path('import/', import_polygon, name='import'),
    path('export/<int:pk>/', export_polygon_to_json, name='export'),
]
