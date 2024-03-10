from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


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
    email = forms.EmailField(label=_("Email"), min_length=6, max_length=128, required=True, widget=EmailInput())
    master_password = forms.CharField(label=_("Master-password"), min_length=8, max_length=128, required=True, widget=PasswordInput())
    tfa_code = forms.CharField(label=_("2FA code (required if 2FA is activated)"), min_length=6, max_length=6, required=False, validators=[
        RegexValidator(regex=r'^\d{6}$', message=_("Enter a valid 6-digit code."))], widget=TextInput())


class RegisterForm(forms.Form):
    email = forms.EmailField(label=_("Email"), min_length=6, max_length=128, required=True, widget=EmailInput())
    master_password = forms.CharField(label=_("Master-password"), min_length=8, max_length=128, required=True, widget=PasswordInput())
