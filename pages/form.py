from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    """
    форма для регистрации пользователя

    поля:
     * username - имя пользователя - виджет: текст - ограничение 50 символов
     * email - адрес эл. почты - виджет: эл. почта
     * password - пароль - виджет: пароль
    """

    username = forms.CharField(
        widget=forms.TextInput, max_length=50, label="Имя пользователя"
    )
    email = forms.EmailField(widget=forms.EmailInput, label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def save(self, commit=True):
        """
        сохраняет данные пользователя в дб
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
