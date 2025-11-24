from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    """Форма для регистрации пользователя"""

    username = forms.CharField(
        widget=forms.TextInput, max_length=15, min_length=3, label="Имя пользователя"
    )
    email = forms.EmailField(widget=forms.EmailInput, label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def save(self, commit=True):
        """Сохраняет данные пользователя в дб"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
