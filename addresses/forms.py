from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from .models import Address


class TextInput(forms.TextInput):
    def __init__(self, attrs=None):
        super().__init__(attrs={'class': 'form-control', **(attrs or {})})


class CheckboxInput(forms.CheckboxInput):
    def __init__(self, attrs=None):
        super().__init__(attrs={'class': 'form-check-input form-check-input-dark', **(attrs or {})})


class Textarea(forms.Textarea):
    def __init__(self, attrs=None):
        super().__init__(attrs={'class': 'form-control', **(attrs or {})})


class AddressMeta:
    @staticmethod
    def get_model():
        return Address

    @staticmethod
    def get_fields():
        return ['title', 'country', 'region', 'locality', 'street', 'house', 'zip_code', 'extra_data', 'init_vector']

    @staticmethod
    def get_widgets(prefix):
        return {
            'title': TextInput(attrs={'id': f'id_{prefix}_title'}),
            'country': TextInput(attrs={'id': f'id_{prefix}_country'}),
            'region': TextInput(attrs={'id': f'id_{prefix}_region'}),
            'locality': TextInput(attrs={'id': f'id_{prefix}_locality'}),
            'street': TextInput(attrs={'id': f'id_{prefix}_street'}),
            'house': TextInput(attrs={'id': f'id_{prefix}_house'}),
            'zip_code': TextInput(attrs={'id': f'id_{prefix}_zip_code'}),
            'extra_data': Textarea(attrs={'id': f'id_{prefix}_extra_data', 'rows': 3}),
            'init_vector': forms.HiddenInput(attrs={'id': f'id_{prefix}_init_vector'})
        }

    @staticmethod
    def get_labels():
        return {
            'title': 'Заголовок',
            'country': 'Страна',
            'region': 'Регион',
            'locality': 'Населенный пункт',
            'street': 'Улица',
            'house': 'Дом',
            'zip_code': 'Индекс',
            'extra_data': 'Дополнительные данные'
        }


class AddAddressForm(forms.ModelForm):
    favorite = forms.BooleanField(label='Избранное', required=False, widget=CheckboxInput(attrs={'id': 'id_add_favorite'}), label_suffix='')

    def __init__(self, *args, **kwargs):
        super(AddAddressForm, self).__init__(*args, **kwargs)

    class Meta:
        model = AddressMeta.get_model()
        fields = AddressMeta.get_fields()
        widgets = AddressMeta.get_widgets('add')
        labels = AddressMeta.get_labels()


class EditAddressForm(forms.ModelForm):
    favorite = forms.BooleanField(label='Избранное', required=False, widget=CheckboxInput(attrs={'id': 'id_edit_favorite'}), label_suffix='')

    def __init__(self, *args, **kwargs):
        super(EditAddressForm, self).__init__(*args, **kwargs)

    class Meta:
        model = AddressMeta.get_model()
        fields = AddressMeta.get_fields()
        widgets = AddressMeta.get_widgets('edit')
        labels = AddressMeta.get_labels()
