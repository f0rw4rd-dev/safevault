from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.generic import View
from django.utils import timezone
from users.models import User
from .models import Bankcard
from .forms import AddBankcardForm, EditBankcardForm
from users.decorators import check_if_user_is_not_authorized, api_check_if_user_is_not_authorized

import json


class BankcardsView(View):
    template_name = 'bankcards/bankcards.html'

    @check_if_user_is_not_authorized
    def get(self, request, *args, **kwargs):
        return self.handle_request(request)

    @check_if_user_is_not_authorized
    def post(self, request, *args, **kwargs):
        operation = request.POST.get('operation')
        bankcard_id = request.POST.get('id')

        try:
            if bankcard_id is not None:
                int(bankcard_id)
        except (TypeError, ValueError):
            return self.handle_request(request)

        if operation == 'add':
            form = AddBankcardForm(request.POST)
            notification_text = 'Запись успешно добавлена'
        elif operation == 'edit' and bankcard_id is not None:
            try:
                bankcard = Bankcard.objects.get(id=bankcard_id, user_id=request.session.get('user_id'))
            except Bankcard.DoesNotExist:
                return self.handle_request(request, notification={'func': 'notifyError', 'text': 'Запись банковской карты не найдена'})

            form = EditBankcardForm(request.POST, instance=bankcard)
            notification_text = 'Запись успешно изменена'
        else:
            return self.handle_request(request)

        if form and form.is_valid():
            bankcard = form.save(commit=False)
            bankcard.user_id = request.session.get('user_id')

            if operation == 'edit' and bankcard.status != form.cleaned_data.get('favorite', False):
                bankcard.change_status_time = timezone.now()

            bankcard.status = form.cleaned_data.get('favorite', False)

            bankcard.save()
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
            bankcards = Bankcard.objects.filter(user=user, status__in=[0, 1]).order_by('-id')
        elif status in [1, 2]:
            bankcards = Bankcard.objects.filter(user=user, status=status).order_by('-id')
        else:
            bankcards = Bankcard.objects.filter(user=user).order_by('-id')

        paginator = Paginator(bankcards, per_page=10)
        page_number = request.GET.get('page', 1)
        bankcards_on_page = paginator.get_page(page_number)

        context = {
            'add_bankcard_form': AddBankcardForm(),
            'edit_bankcard_form': EditBankcardForm(),
            'bankcards': bankcards_on_page,
            'notification': kwargs.get('notification'),
            'status': str(status)
        }

        return render(request, self.template_name, context)


class UpdateBankcardStatusView(View):
    @api_check_if_user_is_not_authorized
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)

            bankcard_id = data.get('id')
            status = data.get('status')

            if bankcard_id is not None and status is not None:
                bankcard_id = int(bankcard_id)
                status = int(status)
            else:
                return HttpResponseBadRequest()
        except (ValueError, TypeError):
            return HttpResponseBadRequest()

        try:
            bankcard = Bankcard.objects.get(id=bankcard_id, user_id=request.session.get('user_id', -1))
        except Bankcard.DoesNotExist:
            return HttpResponseBadRequest()

        bankcard.status = status
        bankcard.change_status_time = timezone.now()
        bankcard.save()

        return JsonResponse({'status': 'ok'})


class DeleteBankcardView(View):
    @api_check_if_user_is_not_authorized
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)

            bankcard_id = data.get('id')

            if bankcard_id is not None:
                bankcard_id = int(bankcard_id)
            else:
                return HttpResponseBadRequest()
        except (ValueError, TypeError):
            return HttpResponseBadRequest()

        try:
            bankcard = Bankcard.objects.get(id=bankcard_id, user_id=request.session.get('user_id'))
        except Bankcard.DoesNotExist:
            return HttpResponseBadRequest()

        bankcard.delete()

        return JsonResponse({'status': 'ok'})
