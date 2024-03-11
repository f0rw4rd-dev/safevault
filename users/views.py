from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.views.generic import View
from .models import User
from .forms import LoginForm, RegisterForm
from .decorators import check_if_user_is_authorized, check_if_user_is_not_authorized


class LoginView(View):
    template_name = 'users/login.html'

    @check_if_user_is_authorized
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    @check_if_user_is_authorized
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)

        if form.is_valid():
            email = request.POST.get('email')
            auth_key = request.POST.get('auth_key')

            user = User.objects.filter(email=email, auth_key=auth_key).first()

            if user:
                request.session['user_id'] = user.id
                return render(request, self.template_name, {'form': form, 'notification': {'func': 'notifySuccess', 'text': 'Вы успешно авторизованы', 'redirectUrl': f'{request.scheme}://{request.get_host()}{reverse('passwords:list')}'}})

            return render(request, self.template_name, {'form': form, 'notification': {'func': 'notifyError', 'text': 'Введены некорректные данные'}})

        return render(request, self.template_name, {'form': form, 'notification': {'func': 'notifyError', 'text': 'Произошла ошибка. Убедитесь, что все поля корректно заполнены'}})


class RegisterView(View):
    template_name = 'users/register.html'

    @check_if_user_is_authorized
    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    @check_if_user_is_authorized
    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']

            if User.objects.filter(email=email).exists():
                return render(request, self.template_name, {'form': form, 'notification': {'func': 'notifyError', 'text': 'Пользователь с данным адресом электронной почты уже существует'}})

            form.save()

            return render(request, self.template_name, {'form': form, 'notification': {'func': 'notifySuccess', 'text': 'Вы успешно зарегистрировались, выполните авторизацию', 'redirectUrl': f'{request.scheme}://{request.get_host()}{reverse('users:login')}'}})

        return render(request, self.template_name, {'form': form, 'notification': {'func': 'notifyError', 'text': 'Произошла ошибка. Убедитесь, что все поля корректно заполнены'}})


class ResetView(View):
    template_name = 'users/reset.html'

    @check_if_user_is_authorized
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class Reset2View(View):
    template_name = 'users/reset-2.html'

    @check_if_user_is_authorized
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        request.session.flush()
        return redirect(reverse('users:login'))


class UserAPIView(View):
    def get(self, request, *args, **kwargs):
        email = request.GET.get('email')

        if not email:
            return JsonResponse({'error': 'Необходимо передать адрес электронной почты'}, status=400)

        try:
            user = User.objects.get(email=email)

            return JsonResponse({'email': user.email, 'salt': user.salt, 'init_vector': user.init_vector})
        except User.DoesNotExist:
            return JsonResponse({'error': 'Пользователь не найден'}, status=404)
