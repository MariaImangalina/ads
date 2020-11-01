from django.forms import ModelForm
from .models import Polygon

class PolygonForm(ModelForm):

    class Meta:
        model = Polygon
        fields = ('name', 'coordinates')
