from django.shortcuts import render

from .forms import PolygonForm
from .models import Polygon

def add_polygon(request):
    form = PolygonForm()

    if request.method == 'POST':
        print('works!')

    return render(request, 'index.html', {'form':form})