from django.urls import path, include

from .views import add_polygon, get_df, DeletePolygon, SearchView, UpdatePolygon, get_df_now, import_polygon

app_name = 'data'

urlpatterns = [
    path('map/', add_polygon, name='map'),
    path('df/', get_df, name='df'),
    path('remove/<int:pk>/', DeletePolygon.as_view(), name='remove'),
    path('search/', SearchView.as_view(), name='search'),
    path('update/<int:pk>/', UpdatePolygon.as_view(), name='update'),
    path('get_now/<int:pk>/', get_df_now, name='get_df_now'),
    path('import/', import_polygon, name='import'),
]
