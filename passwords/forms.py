from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from .models import Password


class TextInput(forms.TextInput):
    def __init__(self, attrs=None):
        super().__init__(attrs={'class': 'form-control', **(attrs or {})})


class CheckboxInput(forms.CheckboxInput):
    def __init__(self, attrs=None):
        super().__init__(attrs={'class': 'form-check-input form-check-input-dark', **(attrs or {})})


class AddPasswordForm(forms.ModelForm):
    favorite = forms.BooleanField(label='Избранное', required=False, widget=CheckboxInput, label_suffix='')

    class Meta:
        model = Password
        fields = ['title', 'website', 'login', 'email', 'password', 'extra_data', 'init_vector']
        widgets = {
            'title': TextInput(attrs={'id': 'id_add_title'}),
            'website': TextInput(attrs={'id': 'id_add_website'}),
            'login': TextInput(attrs={'id': 'id_add_login'}),
            'email': TextInput(attrs={'id': 'id_add_email'}),
            'password': TextInput(attrs={'id': 'id_add_password'}),
            'extra_data': TextInput(attrs={'id': 'id_add_extra_data'}),
            'init_vector': forms.HiddenInput(attrs={'id': 'id_add_init_vector'})
        }
        labels = {
            'title': 'Заголовок',
            'website': 'Веб-сайт',
            'login': 'Логин',
            'email': 'Адрес электронной почты',
            'password': 'Пароль',
            'extra_data': 'Дополнительные данные'
        }
