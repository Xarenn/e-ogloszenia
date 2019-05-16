from django import forms


from .models import User

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='password1', max_length=30, widget=forms.PasswordInput)
    password2 = forms.CharField(label='password2', max_length=30, widget=forms.Textarea)

    class Meta:
        model = User
        fields = ('email',)
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password don't match")
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user