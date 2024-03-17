from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from .models import Bankcard


class TextInput(forms.TextInput):
    def __init__(self, attrs=None):
        super().__init__(attrs={'class': 'form-control', **(attrs or {})})


class CheckboxInput(forms.CheckboxInput):
    def __init__(self, attrs=None):
        super().__init__(attrs={'class': 'form-check-input form-check-input-dark', **(attrs or {})})


class Textarea(forms.Textarea):
    def __init__(self, attrs=None):
        super().__init__(attrs={'class': 'form-control', **(attrs or {})})


class BankcardMeta:
    @staticmethod
    def get_model():
        return Bankcard

    @staticmethod
    def get_fields():
        return ['title', 'card_number', 'card_expiration_month', 'card_expiration_year', 'card_security_code', 'card_pin', 'cardholder_name', 'extra_data', 'init_vector']

    @staticmethod
    def get_widgets(prefix):
        return {
            'title': TextInput(attrs={'id': f'id_{prefix}_title'}),
            'card_number': TextInput(attrs={'id': f'id_{prefix}_card_number'}),
            'card_expiration_month': TextInput(attrs={'id': f'id_{prefix}_card_expiration_month'}),
            'card_expiration_year': TextInput(attrs={'id': f'id_{prefix}_card_expiration_year'}),
            'card_security_code': TextInput(attrs={'id': f'id_{prefix}_card_security_code'}),
            'card_pin': TextInput(attrs={'id': f'id_{prefix}_card_pin'}),
            'cardholder_name': TextInput(attrs={'id': f'id_{prefix}_cardholder_name'}),
            'extra_data': Textarea(attrs={'id': f'id_{prefix}_extra_data', 'rows': 3}),
            'init_vector': forms.HiddenInput(attrs={'id': f'id_{prefix}_init_vector'})
        }

    @staticmethod
    def get_labels():
        return {
            'title': 'Заголовок',
            'card_number': 'Номер карты',
            'card_expiration_month': 'Месяц окончания действия',
            'card_expiration_year': 'Год окончания действия',
            'card_security_code': 'Секретный код',
            'card_pin': 'Пин-код',
            'cardholder_name': 'Владелец',
            'extra_data': 'Дополнительные данные'
        }


class AddBankcardForm(forms.ModelForm):
    favorite = forms.BooleanField(label='Избранное', required=False, widget=CheckboxInput(attrs={'id': 'id_add_favorite'}), label_suffix='')

    def __init__(self, *args, **kwargs):
        super(AddBankcardForm, self).__init__(*args, **kwargs)

    class Meta:
        model = BankcardMeta.get_model()
        fields = BankcardMeta.get_fields()
        widgets = BankcardMeta.get_widgets('add')
        labels = BankcardMeta.get_labels()


class EditBankcardForm(forms.ModelForm):
    favorite = forms.BooleanField(label='Избранное', required=False, widget=CheckboxInput(attrs={'id': 'id_edit_favorite'}), label_suffix='')

    def __init__(self, *args, **kwargs):
        super(EditBankcardForm, self).__init__(*args, **kwargs)

    class Meta:
        model = BankcardMeta.get_model()
        fields = BankcardMeta.get_fields()
        widgets = BankcardMeta.get_widgets('edit')
        labels = BankcardMeta.get_labels()
