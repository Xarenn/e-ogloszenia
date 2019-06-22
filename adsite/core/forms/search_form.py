from django import forms
from core import static_data
from core.models import Ad


class SearchFrom(forms.Form):
    category = forms.ChoiceField(choices=static_data.categories, label='')
    query = forms.CharField(max_length=255, label='')
