from django import forms
from .models import Polygon

class PolygonForm(forms.ModelForm):
    class Meta:
        model = Polygon
        fields = ('name', 'coordinates')
