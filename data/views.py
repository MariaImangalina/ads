from django.shortcuts import render

from .forms import PolygonForm
from .models import Polygon

def add_polygon(request):
    form = PolygonForm()

    if request.is_ajax and request.method == 'POST':
        form = PolygonForm(request.POST)

        if form.is_valid():
            print('works!')


    return render(request, 'data/map.html', {'form':form})