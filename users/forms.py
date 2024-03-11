from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from .models import User


class EmailInput(forms.EmailInput):
    def __init__(self, attrs=None):
        super().__init__(attrs={'class': 'form-control fs-6 py-2', **(attrs or {})})


class PasswordInput(forms.PasswordInput):
    def __init__(self, attrs=None):
        super().__init__(attrs={'class': 'form-control fs-6 py-2', **(attrs or {})})


class TextInput(forms.TextInput):
    def __init__(self, attrs=None):
        super().__init__(attrs={'class': 'form-control fs-6 py-2', **(attrs or {})})


class LoginForm(forms.Form):
    email = forms.EmailField(label="Адрес электронной почты", min_length=6, max_length=128, required=True, widget=EmailInput())
    master_password = forms.CharField(label="Мастер-пароль", min_length=8, max_length=128, required=True, widget=PasswordInput())
    tfa_code = forms.CharField(label="Код 2FA (при наличии)", min_length=6, max_length=6, required=False, validators=[
        RegexValidator(regex=r'^\d{6}$', message="Введите корректный 6-значный код")], widget=TextInput())
    auth_key = forms.CharField(required=True, widget=forms.HiddenInput())


class RegisterForm(forms.Form):
    email = forms.EmailField(label="Адрес электронной почты", min_length=6, max_length=128, required=True, widget=EmailInput())
    master_password = forms.CharField(label="Мастер-пароль", min_length=8, max_length=128, required=True, widget=PasswordInput())
    auth_key = forms.CharField(required=True, widget=forms.HiddenInput())
    salt = forms.CharField(required=True, widget=forms.HiddenInput())
    init_vector = forms.CharField(required=True, widget=forms.HiddenInput())

    def save(self):
        email = self.cleaned_data['email']
        auth_key = self.cleaned_data['auth_key']
        salt = self.cleaned_data['salt']
        init_vector = self.cleaned_data['init_vector']

        user = User(
            email=email,
            auth_key=auth_key,
            salt=salt,
            init_vector=init_vector,
            is_active=True
        )

        user.save()

        return user
