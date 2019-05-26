from django import forms
from .models import User

class DetailsForm(forms.ModelForm):
    name = forms.CharField()
    phone = forms.CharField()

    class Meta:
        model = User
        fields = ('name', 'phone',)
    

    def save(self, commit=True):
        user = super(DetailsForm, self).save(commit=False)
        user.name = self.cleaned_data['name']
        user.phone = self.cleaned_data['phone']

        if commit:
            user.save()
        
        return user
