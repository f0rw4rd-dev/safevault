from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from .models import Document


class TextInput(forms.TextInput):
    def __init__(self, attrs=None):
        super().__init__(attrs={'class': 'form-control', **(attrs or {})})


class Textarea(forms.Textarea):
    def __init__(self, attrs=None):
        super().__init__(attrs={'class': 'form-control', **(attrs or {})})


class CheckboxInput(forms.CheckboxInput):
    def __init__(self, attrs=None):
        super().__init__(attrs={'class': 'form-check-input form-check-input-dark', **(attrs or {})})


class DocumentMeta:
    @staticmethod
    def get_model():
        return Document

    @staticmethod
    def get_fields():
        return ['title', 'document_number', 'issuing_authority', 'issue_date', 'expiration_date', 'extra_data', 'init_vector']

    @staticmethod
    def get_widgets(prefix):
        return {
            'title': TextInput(attrs={'id': f'id_{prefix}_title'}),
            'document_number': TextInput(attrs={'id': f'id_{prefix}_document_number'}),
            'issuing_authority': TextInput(attrs={'id': f'id_{prefix}_issuing_authority'}),
            'issue_date': forms.HiddenInput(attrs={'id': f'id_{prefix}_issue_date'}),
            'expiration_date': forms.HiddenInput(attrs={'id': f'id_{prefix}_expiration_date'}),
            'extra_data': Textarea(attrs={'id': f'id_{prefix}_extra_data', 'rows': 3}),
            'init_vector': forms.HiddenInput(attrs={'id': f'id_{prefix}_init_vector'})
        }

    @staticmethod
    def get_labels():
        return {
            'title': 'Заголовок',
            'document_number': 'Номер документа',
            'issuing_authority': 'Орган выдачи',
            'issue_date': 'Дата выдачи',
            'expiration_date': 'Срок действия',
            'extra_data': 'Дополнительные данные',
        }


class AddDocumentForm(forms.ModelForm):
    favorite = forms.BooleanField(label='Избранное', required=False, widget=CheckboxInput(attrs={'id': 'id_add_favorite'}), label_suffix='')

    def __init__(self, *args, **kwargs):
        super(AddDocumentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DocumentMeta.get_model()
        fields = DocumentMeta.get_fields()
        widgets = DocumentMeta.get_widgets('add')
        labels = DocumentMeta.get_labels()


class EditDocumentForm(forms.ModelForm):
    favorite = forms.BooleanField(label='Избранное', required=False, widget=CheckboxInput(attrs={'id': 'id_edit_favorite'}), label_suffix='')

    def __init__(self, *args, **kwargs):
        super(EditDocumentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DocumentMeta.get_model()
        fields = DocumentMeta.get_fields()
        widgets = DocumentMeta.get_widgets('edit')
        labels = DocumentMeta.get_labels()
