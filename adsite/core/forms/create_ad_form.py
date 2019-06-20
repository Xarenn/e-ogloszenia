from django import forms
from core import static_data
from core.models import Ad


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'category', 'short_description', 'personality', 'price', 'description', ]

    title = forms.CharField(max_length=255, min_length=5)
    category = forms.ChoiceField(choices=static_data.categories)
    short_description = forms.CharField(max_length=120)
    personality = forms.ChoiceField(choices=static_data.personality)
    description = forms.CharField(widget=forms.Textarea)
    price = forms.FloatField()
