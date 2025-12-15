from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=15,
        min_length=3,
        label="Имя пользователя",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )   

    def save(self):
        if not self.is_valid():
            raise ValueError("ValueError")
        user = User(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email']
        )
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user


