from django.shortcuts import render

from .forms import PolygonForm
from .models import Polygon

### преобразуем координаты из Array в формат запроса SQL
def to_sql(coordinates):
    cor = [i.strip('),').replace(', ', ' ').strip() for i in coordinates.split('LatLng(')[1:]]
    cor1 = [i.split(' ') for i in (cor + [cor[0]])]
    for i in cor1:
        i.reverse()
    cor2 = [' '.join(i) for i in cor1]
    cor3 = ','.join(cor2)
    return cor3



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