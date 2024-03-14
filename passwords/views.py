from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.generic import View
from users.models import User
from .models import Password
from .forms import AddPasswordForm, EditPasswordForm
from users.decorators import check_if_user_is_not_authorized


class PasswordsView(View):
    template_name = 'passwords/passwords.html'

    @check_if_user_is_not_authorized
    def get(self, request, *args, **kwargs):
        user = User.objects.filter(id=request.session.get('user_id')).first()
        passwords = Password.objects.filter(user=user).order_by('-id')
        paginator = Paginator(passwords, per_page=10)

        page_number = request.GET.get('page', 1)
        passwords_on_page = paginator.get_page(page_number)

        add_password_form = AddPasswordForm()
        edit_password_form = EditPasswordForm()
        return render(request, self.template_name, {'add_password_form': add_password_form, 'edit_password_form': edit_password_form, 'passwords': passwords_on_page})

    @check_if_user_is_not_authorized
    def post(self, request, *args, **kwargs):
        operation = request.POST.get('operation')

        user = User.objects.filter(id=request.session.get('user_id')).first()
        passwords = Password.objects.filter(user=user).order_by('-id')
        paginator = Paginator(passwords, per_page=10)

        page_number = request.GET.get('page', 1)
        passwords_on_page = paginator.get_page(page_number)

        password_id = request.POST.get('id')

        if operation == 'add':
            password_form = AddPasswordForm(request.POST)
            notification = 'Запись успешно добавлена'
        elif operation == 'edit' and password_id is not None:
            password_form = EditPasswordForm(request.POST, instance=Password.objects.get(id=password_id))
            notification = 'Запись успешно изменена'
        else:
            return render(request, self.template_name, {'add_password_form': AddPasswordForm(), 'edit_password_form': EditPasswordForm(), 'passwords': passwords_on_page, 'notification': {'func': 'notifyError', 'text': 'Произошла ошибка. Убедитесь, что все поля корректно заполнены'}})

        if password_form.is_valid():
            password = password_form.save(commit=False)
            password.user_id = request.session.get('user_id')
            password.status = password_form.cleaned_data.get('favorite')
            password.save()
            return render(request, self.template_name, {'add_password_form': AddPasswordForm(), 'edit_password_form': EditPasswordForm(), 'passwords': passwords_on_page, 'notification': {'func': 'notifySuccess', 'text': notification, 'redirectUrl': f'{request.scheme}://{request.get_host()}{reverse('passwords:passwords')}'}})

        return render(request, self.template_name, {'add_password_form': AddPasswordForm(), 'edit_password_form': EditPasswordForm(), 'passwords': passwords_on_page, 'notification': {'func': 'notifyError', 'text': 'Произошла ошибка. Убедитесь, что все поля корректно заполнены'}})
