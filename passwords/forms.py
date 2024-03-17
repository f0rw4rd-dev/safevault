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


class Textarea(forms.Textarea):
    def __init__(self, attrs=None):
        super().__init__(attrs={'class': 'form-control', **(attrs or {})})


class PasswordMeta:
    @staticmethod
    def get_model():
        return Password

    @staticmethod
    def get_fields():
        return ['title', 'website', 'login', 'email', 'password', 'extra_data', 'init_vector']

    @staticmethod
    def get_widgets(prefix):
        return {
            'title': TextInput(attrs={'id': f'id_{prefix}_title'}),
            'website': TextInput(attrs={'id': f'id_{prefix}_website'}),
            'login': TextInput(attrs={'id': f'id_{prefix}_login'}),
            'email': TextInput(attrs={'id': f'id_{prefix}_email'}),
            'password': TextInput(attrs={'id': f'id_{prefix}_password'}),
            'extra_data': Textarea(attrs={'id': f'id_{prefix}_extra_data', 'rows': 3}),
            'init_vector': forms.HiddenInput(attrs={'id': f'id_{prefix}_init_vector'})
        }

    @staticmethod
    def get_labels():
        return {
            'title': 'Заголовок',
            'website': 'Веб-сайт',
            'login': 'Логин',
            'email': 'Адрес электронной почты',
            'password': 'Пароль',
            'extra_data': 'Дополнительные данные'
        }


class AddPasswordForm(forms.ModelForm):
    favorite = forms.BooleanField(label='Избранное', required=False, widget=CheckboxInput(attrs={'id': 'id_add_favorite'}), label_suffix='')

    def __init__(self, *args, **kwargs):
        super(AddPasswordForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PasswordMeta.get_model()
        fields = PasswordMeta.get_fields()
        widgets = PasswordMeta.get_widgets('add')
        labels = PasswordMeta.get_labels()


class EditPasswordForm(forms.ModelForm):
    favorite = forms.BooleanField(label='Избранное', required=False, widget=CheckboxInput(attrs={'id': 'id_edit_favorite'}), label_suffix='')

    def __init__(self, *args, **kwargs):
        super(EditPasswordForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PasswordMeta.get_model()
        fields = PasswordMeta.get_fields()
        widgets = PasswordMeta.get_widgets('edit')
        labels = PasswordMeta.get_labels()
