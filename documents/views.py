from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.generic import View
from django.utils import timezone
from users.models import User
from .models import Document
from .forms import AddDocumentForm, EditDocumentForm
from users.decorators import check_if_user_is_not_authorized, api_check_if_user_is_not_authorized

import json


class DocumentsView(View):
    template_name = 'documents/documents.html'

    @check_if_user_is_not_authorized
    def get(self, request, *args, **kwargs):
        return self.handle_request(request)

    @check_if_user_is_not_authorized
    def post(self, request, *args, **kwargs):
        operation = request.POST.get('operation')
        document_id = request.POST.get('id')

        try:
            if document_id is not None:
                int(document_id)
        except (TypeError, ValueError):
            return self.handle_request(request)

        if operation == 'add':
            form = AddDocumentForm(request.POST)
            notification_text = 'Запись успешно добавлена'
        elif operation == 'edit' and document_id is not None:
            try:
                document = Document.objects.get(id=document_id, user_id=request.session.get('user_id'))
            except Document.DoesNotExist:
                return self.handle_request(request, notification={'func': 'notifyError', 'text': 'Запись документа не найдена'})

            form = EditDocumentForm(request.POST, instance=document)
            notification_text = 'Запись успешно изменена'
        else:
            return self.handle_request(request)

        if form and form.is_valid():
            document = form.save(commit=False)
            document.user_id = request.session.get('user_id')

            if operation == 'edit' and document.status != form.cleaned_data.get('favorite', False):
                document.change_status_time = timezone.now()

            document.status = form.cleaned_data.get('favorite', False)

            document.save()
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
            documents = Document.objects.filter(user=user, status__in=[0, 1]).order_by('-id')
        elif status in [1, 2]:
            documents = Document.objects.filter(user=user, status=status).order_by('-id')
        else:
            documents = Document.objects.filter(user=user).order_by('-id')

        paginator = Paginator(documents, per_page=10)
        page_number = request.GET.get('page', 1)
        documents_on_page = paginator.get_page(page_number)

        context = {
            'add_document_form': AddDocumentForm(),
            'edit_document_form': EditDocumentForm(),
            'documents': documents_on_page,
            'notification': kwargs.get('notification'),
            'status': str(status)
        }

        return render(request, self.template_name, context)


class UpdateDocumentStatusView(View):
    @api_check_if_user_is_not_authorized
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)

            document_id = data.get('id')
            status = data.get('status')

            if document_id is not None and status is not None:
                document_id = int(document_id)
                status = int(status)
            else:
                return HttpResponseBadRequest()
        except (ValueError, TypeError):
            return HttpResponseBadRequest()

        try:
            document = Document.objects.get(id=document_id, user_id=request.session.get('user_id', -1))
        except Document.DoesNotExist:
            return HttpResponseBadRequest()

        document.status = status
        document.change_status_time = timezone.now()
        document.save()

        return JsonResponse({'status': 'ok'})


class DeleteDocumentView(View):
    @api_check_if_user_is_not_authorized
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)

            document_id = data.get('id')

            if document_id is not None:
                document_id = int(document_id)
            else:
                return HttpResponseBadRequest()
        except (ValueError, TypeError):
            return HttpResponseBadRequest()

        try:
            document = Document.objects.get(id=document_id, user_id=request.session.get('user_id'))
        except Document.DoesNotExist:
            return HttpResponseBadRequest()

        document.delete()

        return JsonResponse({'status': 'ok'})
