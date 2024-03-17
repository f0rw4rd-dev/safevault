from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.generic import View
from django.utils import timezone
from users.models import User
from .models import Address
from .forms import AddAddressForm, EditAddressForm
from users.decorators import check_if_user_is_not_authorized, api_check_if_user_is_not_authorized

import json


class AddressesView(View):
    template_name = 'addresses/addresses.html'

    @check_if_user_is_not_authorized
    def get(self, request, *args, **kwargs):
        return self.handle_request(request)

    @check_if_user_is_not_authorized
    def post(self, request, *args, **kwargs):
        operation = request.POST.get('operation')
        address_id = request.POST.get('id')

        try:
            if address_id is not None:
                int(address_id)
        except (TypeError, ValueError):
            return self.handle_request(request)

        if operation == 'add':
            form = AddAddressForm(request.POST)
            notification_text = 'Запись успешно добавлена'
        elif operation == 'edit' and address_id is not None:
            try:
                address = Address.objects.get(id=address_id, user_id=request.session.get('user_id'))
            except Address.DoesNotExist:
                return self.handle_request(request, notification={'func': 'notifyError', 'text': 'Запись адреса не найдена'})

            form = EditAddressForm(request.POST, instance=address)
            notification_text = 'Запись успешно изменена'
        else:
            return self.handle_request(request)

        if form and form.is_valid():
            address = form.save(commit=False)
            address.user_id = request.session.get('user_id')

            if operation == 'edit' and address.status != form.cleaned_data.get('favorite', False):
                address.change_status_time = timezone.now()

            address.status = form.cleaned_data.get('favorite', False)

            address.save()
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
            addresses = Address.objects.filter(user=user, status__in=[0, 1]).order_by('-id')
        elif status in [1, 2]:
            addresses = Address.objects.filter(user=user, status=status).order_by('-id')
        else:
            addresses = Address.objects.filter(user=user).order_by('-id')

        paginator = Paginator(addresses, per_page=10)
        page_number = request.GET.get('page', 1)
        addresses_on_page = paginator.get_page(page_number)

        context = {
            'add_address_form': AddAddressForm(),
            'edit_address_form': EditAddressForm(),
            'addresses': addresses_on_page,
            'notification': kwargs.get('notification'),
            'status': str(status)
        }

        return render(request, self.template_name, context)


class UpdateAddressStatusView(View):
    @api_check_if_user_is_not_authorized
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)

            address_id = data.get('id')
            status = data.get('status')

            if address_id is not None and status is not None:
                address_id = int(address_id)
                status = int(status)
            else:
                return HttpResponseBadRequest()
        except (ValueError, TypeError):
            return HttpResponseBadRequest()

        try:
            address = Address.objects.get(id=address_id, user_id=request.session.get('user_id', -1))
        except Address.DoesNotExist:
            return HttpResponseBadRequest()

        address.status = status
        address.change_status_time = timezone.now()
        address.save()

        return JsonResponse({'status': 'ok'})


class DeleteAddressView(View):
    @api_check_if_user_is_not_authorized
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)

            address_id = data.get('id')

            if address_id is not None:
                address_id = int(address_id)
            else:
                return HttpResponseBadRequest()
        except (ValueError, TypeError):
            return HttpResponseBadRequest()

        try:
            address = Address.objects.get(id=address_id, user_id=request.session.get('user_id'))
        except Address.DoesNotExist:
            return HttpResponseBadRequest()

        address.delete()

        return JsonResponse({'status': 'ok'})
