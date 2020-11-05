from django.shortcuts import render

from .forms import PolygonForm
from .models import Polygon

def add_polygon(request):
    form = PolygonForm()

    if request.is_ajax and request.method == 'POST':
        formset = PolygonForm(request.POST)
        print('works here')

        if formset.is_valid():
            polygon = formset.save(commit=False)
            polygon.user = request.user
            polygon.save()
            print('works!')
        else:
            print(formset.errors)


    return render(request, 'data/map.html', {'form':form})