from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from .models import Note


class TextInput(forms.TextInput):
    def __init__(self, attrs=None):
        super().__init__(attrs={'class': 'form-control', **(attrs or {})})


class Textarea(forms.Textarea):
    def __init__(self, attrs=None):
        super().__init__(attrs={'class': 'form-control', **(attrs or {})})


class CheckboxInput(forms.CheckboxInput):
    def __init__(self, attrs=None):
        super().__init__(attrs={'class': 'form-check-input form-check-input-dark', **(attrs or {})})


class NoteMeta:
    @staticmethod
    def get_model():
        return Note

    @staticmethod
    def get_fields():
        return ['title', 'data', 'init_vector']

    @staticmethod
    def get_widgets(prefix):
        return {
            'title': TextInput(attrs={'id': f'id_{prefix}_title'}),
            'data': Textarea(attrs={'id': f'id_{prefix}_data', 'rows': 5}),
            'init_vector': forms.HiddenInput(attrs={'id': f'id_{prefix}_init_vector'})
        }

    @staticmethod
    def get_labels():
        return {
            'title': 'Заголовок',
            'data': 'Содержание'
        }


class AddNoteForm(forms.ModelForm):
    favorite = forms.BooleanField(label='Избранное', required=False, widget=CheckboxInput(attrs={'id': 'id_add_favorite'}), label_suffix='')

    def __init__(self, *args, **kwargs):
        super(AddNoteForm, self).__init__(*args, **kwargs)

    class Meta:
        model = NoteMeta.get_model()
        fields = NoteMeta.get_fields()
        widgets = NoteMeta.get_widgets('add')
        labels = NoteMeta.get_labels()


class EditNoteForm(forms.ModelForm):
    favorite = forms.BooleanField(label='Избранное', required=False, widget=CheckboxInput(attrs={'id': 'id_edit_favorite'}), label_suffix='')

    def __init__(self, *args, **kwargs):
        super(EditNoteForm, self).__init__(*args, **kwargs)

    class Meta:
        model = NoteMeta.get_model()
        fields = NoteMeta.get_fields()
        widgets = NoteMeta.get_widgets('edit')
        labels = NoteMeta.get_labels()
