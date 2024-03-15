from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.generic import View
from django.utils import timezone
from users.models import User
from .models import Password
from .forms import AddPasswordForm, EditPasswordForm
from users.decorators import check_if_user_is_not_authorized


class PasswordsView(View):
    template_name = 'passwords/passwords.html'

    @check_if_user_is_not_authorized
    def get(self, request, *args, **kwargs):
        return self.handle_request(request, new_form=True)

    @check_if_user_is_not_authorized
    def post(self, request, *args, **kwargs):
        operation = request.POST.get('operation')
        password_id = request.POST.get('id')

        try:
            if password_id is not None:
                int(password_id)
        except (TypeError, ValueError):
            return self.handle_request(request)

        if operation == 'add':
            form = AddPasswordForm(request.POST)
            notification_text = 'Запись успешно добавлена'
        elif operation == 'edit' and password_id is not None:
            try:
                password = Password.objects.get(id=password_id, user_id=request.session.get('user_id'))
            except Password.DoesNotExist:
                return self.handle_request(request, notification={'func': 'notifyError', 'text': 'Запись пароля не найдена'})

            form = EditPasswordForm(request.POST, instance=password)
            notification_text = 'Запись успешно изменена'
        else:
            return self.handle_request(request)

        if form and form.is_valid():
            password = form.save(commit=False)
            password.user_id = request.session.get('user_id')
            password.status = form.cleaned_data.get('favorite', False)

            if operation == 'edit':
                password.change_status_time = timezone.now()

            password.save()
            return self.handle_request(request, notification={'func': 'notifySuccess', 'text': notification_text})
        else:
            notification = {'func': 'notifyError', 'text': 'Произошла ошибка. Убедитесь, что все поля корректно заполнены'} if form else None
            return self.handle_request(request, notification=notification)

    def handle_request(self, request, **kwargs):
        user = User.objects.get(id=request.session.get('user_id'))

        try:
            status = int(request.GET.get('status', '0'))
        except (TypeError, ValueError):
            status = 0

        if status == 0:
            passwords = Password.objects.filter(user=user, status__in=[0, 1]).order_by('-id')
        elif status in [1, 2]:
            passwords = Password.objects.filter(user=user, status=status).order_by('-id')
        else:
            passwords = Password.objects.filter(user=user).order_by('-id')

        paginator = Paginator(passwords, per_page=10)
        page_number = request.GET.get('page', 1)
        passwords_on_page = paginator.get_page(page_number)

        context = {
            'add_password_form': AddPasswordForm(),
            'edit_password_form': EditPasswordForm(),
            'passwords': passwords_on_page,
            'notification': kwargs.get('notification'),
            'status': str(status)
        }

        return render(request, self.template_name, context)

# class PasswordsView(View):
#     template_name = 'passwords/passwords.html'
#
#     @check_if_user_is_not_authorized
#     def get(self, request, *args, **kwargs):
#         user = User.objects.filter(id=request.session.get('user_id')).first()
#         passwords = Password.objects.filter(user=user).order_by('-id')
#         paginator = Paginator(passwords, per_page=10)
#
#         page_number = request.GET.get('page', 1)
#         passwords_on_page = paginator.get_page(page_number)
#
#         add_password_form = AddPasswordForm()
#         edit_password_form = EditPasswordForm()
#         return render(request, self.template_name, {'add_password_form': add_password_form, 'edit_password_form': edit_password_form, 'passwords': passwords_on_page})
#
#     @check_if_user_is_not_authorized
#     def post(self, request, *args, **kwargs):
#         operation = request.POST.get('operation')
#         user = User.objects.filter(id=request.session.get('user_id')).first()
#
#         passwords = Password.objects.filter(user=user).order_by('-id')
#         paginator = Paginator(passwords, per_page=10)
#
#         page_number = request.GET.get('page', 1)
#         passwords_on_page = paginator.get_page(page_number)
#
#         password_id = request.POST.get('id')
#
#         if operation == 'add':
#             password_form = AddPasswordForm(request.POST)
#             notification = 'Запись успешно добавлена'
#         elif operation == 'edit' and password_id is not None:
#             password_form = EditPasswordForm(request.POST, instance=Password.objects.get(id=password_id))
#             notification = 'Запись успешно изменена'
#         else:
#             return render(request, self.template_name, {'add_password_form': AddPasswordForm(), 'edit_password_form': EditPasswordForm(), 'passwords': passwords_on_page, 'notification': {'func': 'notifyError', 'text': 'Произошла ошибка. Убедитесь, что все поля корректно заполнены'}})
#
#         if password_form.is_valid():
#             password = password_form.save(commit=False)
#             password.user_id = request.session.get('user_id')
#             password.status = password_form.cleaned_data.get('favorite')
#             password.save()
#
#             passwords = Password.objects.filter(user=user).order_by('-id')
#             paginator = Paginator(passwords, per_page=10)
#
#             page_number = request.GET.get('page', 1)
#             passwords_on_page = paginator.get_page(page_number)
#
#             return render(request, self.template_name, {'add_password_form': AddPasswordForm(), 'edit_password_form': EditPasswordForm(), 'passwords': passwords_on_page, 'notification': {'func': 'notifySuccess', 'text': notification, 'redirectUrl': f'{request.scheme}://{request.get_host()}{reverse('passwords:passwords')}'}})
#
#         return render(request, self.template_name, {'add_password_form': AddPasswordForm(), 'edit_password_form': EditPasswordForm(), 'passwords': passwords_on_page, 'notification': {'func': 'notifyError', 'text': 'Произошла ошибка. Убедитесь, что все поля корректно заполнены'}})
