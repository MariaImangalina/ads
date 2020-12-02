from django import forms
from .models import Polygon

class PolygonForm(forms.ModelForm):
    
    class Meta:
        model = Polygon
        fields = ('name', 'ads_type', 'min_area', 'max_area', 'coordinates')
        widgets = {'coordinates': forms.HiddenInput()}


class SearchPolygon(forms.Form):
    query = forms.CharField(max_length=256)


class PolygonImportForm(forms.ModelForm):
    coord_file = forms.FileField()

    class Meta:
        model = Polygon
        fields = ('name', 'ads_type', 'min_area', 'max_area', 'coord_file')
    


