from django.urls import path, include

from .views import add_polygon, get_df, DeletePolygon, SearchView


app_name = 'data'

urlpatterns = [
    path('map/', add_polygon, name='map'),
    path('df/', get_df, name='df'),
    path('remove/<int:pk>/', DeletePolygon.as_view(), name='remove'),
    path('search/', SearchView.as_view(), name='search'),
]
