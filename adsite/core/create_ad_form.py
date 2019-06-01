from django import forms

categories = [
    ('Electronics', 'Electronics'),
]

personality = [
    ('Private Person', 'Private Person'),
    ('Company', 'Company'),
]

class AdForm(forms.Form):
    title = forms.CharField(max_length=255, min_length=5)
    category = forms.ChoiceField(choices=categories)
    short_description = forms.CharField(max_length=120)
    personality = forms.ChoiceField(choices=personality)
    description = forms.CharField(widget=forms.Textarea)
    price = forms.FloatField()


