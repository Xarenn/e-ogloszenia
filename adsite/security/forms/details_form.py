from django import forms

from core.services.client_service import request_post
from security.auth.api_urls import UPDATE_USER
from security.models import User


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

        data = {
            "login": user.email,
            "password": user.password,
            "UPDATE": {
                "name": user.name,
                "phone": user.phone
            }
        }
        response = request_post(UPDATE_USER, data)

        if response.status_code == 200:
            if commit:
                user.save()

        return user
