from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.generic import View
from django.utils import timezone
from users.models import User
from .models import Note
from .forms import AddNoteForm, EditNoteForm
from users.decorators import check_if_user_is_not_authorized, api_check_if_user_is_not_authorized

import json


class NotesView(View):
    template_name = 'notes/notes.html'

    @check_if_user_is_not_authorized
    def get(self, request, *args, **kwargs):
        return self.handle_request(request)

    @check_if_user_is_not_authorized
    def post(self, request, *args, **kwargs):
        operation = request.POST.get('operation')
        note_id = request.POST.get('id')

        try:
            if note_id is not None:
                int(note_id)
        except (TypeError, ValueError):
            return self.handle_request(request)

        if operation == 'add':
            form = AddNoteForm(request.POST)
            notification_text = 'Запись успешно добавлена'
        elif operation == 'edit' and note_id is not None:
            try:
                note = Note.objects.get(id=note_id, user_id=request.session.get('user_id'))
            except Note.DoesNotExist:
                return self.handle_request(request, notification={'func': 'notifyError', 'text': 'Запись заметки не найдена'})

            form = EditNoteForm(request.POST, instance=note)
            notification_text = 'Запись успешно изменена'
        else:
            return self.handle_request(request)

        if form and form.is_valid():
            note = form.save(commit=False)
            note.user_id = request.session.get('user_id')

            if operation == 'edit' and note.status != form.cleaned_data.get('favorite', False):
                note.change_status_time = timezone.now()

            note.status = form.cleaned_data.get('favorite', False)

            note.save()
            return self.handle_request(request, notification={'func': 'notifySuccess', 'text': notification_text})
        else:
            notification = {'func': 'notifyError', 'text': 'Убедитесь, что все поля корректно заполнены'} if form else None
            return self.handle_request(request, notification=notification)

    def handle_request(self, request, **kwargs):
        user = User.objects.get(id=request.session.get('user_id'))

        try:
            status = int(request.GET.get('status', '0'))
        except (TypeError, ValueError):
            status = 0

        if status == 0:
            notes = Note.objects.filter(user=user, status__in=[0, 1]).order_by('-id')
        elif status in [1, 2]:
            notes = Note.objects.filter(user=user, status=status).order_by('-id')
        else:
            notes = Note.objects.filter(user=user).order_by('-id')

        paginator = Paginator(notes, per_page=10)
        page_number = request.GET.get('page', 1)
        notes_on_page = paginator.get_page(page_number)

        context = {
            'add_note_form': AddNoteForm(),
            'edit_note_form': EditNoteForm(),
            'notes': notes_on_page,
            'notification': kwargs.get('notification'),
            'status': str(status)
        }

        return render(request, self.template_name, context)


class UpdateNoteStatusView(View):
    @api_check_if_user_is_not_authorized
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)

            note_id = data.get('id')
            status = data.get('status')

            if note_id is not None and status is not None:
                note_id = int(note_id)
                status = int(status)
            else:
                return HttpResponseBadRequest()
        except (ValueError, TypeError):
            return HttpResponseBadRequest()

        try:
            note = Note.objects.get(id=note_id, user_id=request.session.get('user_id', -1))
        except Note.DoesNotExist:
            return HttpResponseBadRequest()

        note.status = status
        note.change_status_time = timezone.now()
        note.save()

        return JsonResponse({'status': 'ok'})


class DeleteNoteView(View):
    @api_check_if_user_is_not_authorized
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)

            note_id = data.get('id')

            if note_id is not None:
                note_id = int(note_id)
            else:
                return HttpResponseBadRequest()
        except (ValueError, TypeError):
            return HttpResponseBadRequest()

        try:
            note = Note.objects.get(id=note_id, user_id=request.session.get('user_id'))
        except Note.DoesNotExist:
            return HttpResponseBadRequest()

        note.delete()

        return JsonResponse({'status': 'ok'})
