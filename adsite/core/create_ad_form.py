from django import forms
from . import static_data

class AdForm(forms.Form):
    title = forms.CharField(max_length=255, min_length=5)
    category = forms.ChoiceField(choices=static_data.categories)
    short_description = forms.CharField(max_length=120)
    personality = forms.ChoiceField(choices=static_data.personality)
    description = forms.CharField(widget=forms.Textarea)
    price = forms.FloatField()
    