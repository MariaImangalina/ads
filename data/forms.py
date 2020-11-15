from django import forms
from .models import Polygon

class PolygonForm(forms.ModelForm):
    
    class Meta:
        model = Polygon
        fields = ('name', 'coordinates')
        widgets = {'coordinates': forms.HiddenInput()}


class SearchPolygon(forms.Form):
    query = forms.CharField(max_length=256)
