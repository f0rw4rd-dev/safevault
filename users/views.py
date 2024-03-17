from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.utils import timezone
from django.views.generic import View
from django.core.mail import send_mail
from .models import User
from .forms import LoginForm, RegisterForm, ResetForm
from .decorators import check_if_user_is_authorized, check_if_user_is_not_authorized
from io import BytesIO

import pyotp
import qrcode
import base64
import re
import secrets


class LoginView(View):
    template_name = 'users/login.html'

    @check_if_user_is_authorized
    def get(self, request, *args, **kwargs):
        login_form = LoginForm()
        return render(request, self.template_name, {'login_form': login_form})

    @check_if_user_is_authorized
    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            email = request.POST.get('email')
            auth_key = request.POST.get('auth_key')

            user = User.objects.filter(email=email, auth_key=auth_key).first()

            def ban_if_no_more_attempts(email):
                try:
                    user = User.objects.get(email=email)

                    if user.auth_attempts == 1:
                        user.auth_lock_end_time = timezone.now() + timezone.timedelta(minutes=30)

                    if user.auth_attempts >= 1:
                        user.auth_attempts -= 1

                    user.auth_last_attempt_time = timezone.now()
                    user.save()
                except User.DoesNotExist:
                    pass

            def reset_attempts(user):
                user.auth_attempts = 3
                user.save()

            if user:
                if not user.is_active:
                    notification_text = 'Пользователь заблокирован'
                    return render(request, self.template_name, {'login_form': LoginForm(), 'notification': {'func': 'notifyError', 'text': notification_text}})

                if timezone.now() - user.auth_last_attempt_time > timezone.timedelta(minutes=30) or timezone.now() > user.auth_lock_end_time and user.auth_attempts == 0:
                    reset_attempts(user)

                if timezone.now() < user.auth_lock_end_time:
                    notification_text = 'Превышено количество попыток авторизации, подождите окончания блокировки'
                    return render(request, self.template_name, {'login_form': LoginForm(), 'notification': {'func': 'notifyError', 'text': notification_text}})

                if user.tfa_key is not None:
                    tfa_code = request.POST.get('tfa_code')

                    if not tfa_code:
                        notification_text = 'Введите код для двухфакторной аутентификации'
                        return render(request, self.template_name, {'login_form': LoginForm(), 'notification': {'func': 'notifyError', 'text': notification_text}})

                    if not pyotp.TOTP(user.tfa_key).verify(tfa_code):
                        ban_if_no_more_attempts(email)
                        notification_text = 'Введен неверный код'
                        return render(request, self.template_name, {'login_form': LoginForm(), 'notification': {'func': 'notifyError', 'text': notification_text}})

                request.session.set_expiry(user.session_duration * 60)
                request.session['user_id'] = user.id

                notification_text = 'Вы успешно авторизованы'
                notification_redirect_url = f'{request.scheme}://{request.get_host()}{reverse('passwords:passwords')}'
                return render(request, self.template_name, {'login_form': LoginForm(), 'notification': {'func': 'notifySuccess', 'text': notification_text, 'redirectUrl': notification_redirect_url}})

            try:
                user = User.objects.get(email=email)

                if timezone.now() < user.auth_lock_end_time:
                    notification_text = 'Превышено количество попыток авторизации, подождите окончания блокировки'
                    return render(request, self.template_name, {'login_form': LoginForm(), 'notification': {'func': 'notifyError', 'text': notification_text}})
            except User.DoesNotExist:
                notification_text = 'Введены некорректные данные'
                return render(request, self.template_name, {'login_form': LoginForm(), 'notification': {'func': 'notifyError', 'text': notification_text}})

            ban_if_no_more_attempts(email)
            notification_text = 'Введены некорректные данные'
            return render(request, self.template_name, {'login_form': LoginForm(), 'notification': {'func': 'notifyError', 'text': notification_text}})

        notification_text = 'Убедитесь, что все поля корректно заполнены'
        return render(request, self.template_name, {'login_form': LoginForm(), 'notification': {'func': 'notifyError', 'text': notification_text}})


class RegisterView(View):
    template_name = 'users/register.html'

    @check_if_user_is_authorized
    def get(self, request, *args, **kwargs):
        register_form = RegisterForm()
        return render(request, self.template_name, {'register_form': register_form})

    @check_if_user_is_authorized
    def post(self, request, *args, **kwargs):
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            email = register_form.cleaned_data['email']

            if User.objects.filter(email=email).exists():
                notification_text = 'Пользователь с данным адресом электронной почты уже существует'
                return render(request, self.template_name, {'register_form': RegisterForm(), 'notification': {'func': 'notifyError', 'text': notification_text}})

            register_form.save()

            notification_text = 'Вы успешно зарегистрировались, выполните авторизацию'
            notification_redirect_url = f'{request.scheme}://{request.get_host()}{reverse('users:login')}'
            return render(request, self.template_name, {'register_form': RegisterForm(), 'notification': {'func': 'notifySuccess', 'text': notification_text, 'redirectUrl': notification_redirect_url}})

        notification_text = 'Убедитесь, что все поля корректно заполнены'
        return render(request, self.template_name, {'register_form': RegisterForm(), 'notification': {'func': 'notifyError', 'text': notification_text}})


class ResetView(View):
    template_name = 'users/reset.html'

    @check_if_user_is_authorized
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'reset_form': ResetForm()})

    @check_if_user_is_authorized
    def post(self, request, *args, **kwargs):
        form = ResetForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']

            try:
                user = User.objects.get(email=email)
                user.resetpassword_set.all().delete()

                reset_key = secrets.token_hex(64)
                reset_password = user.resetpassword_set.create(reset_key=reset_key)
                reset_link = request.build_absolute_uri(reverse('users:reset-confirm', args=[reset_key]))

                send_mail(
                    'Сброс пароля',
                    f'Перейдите по ссылке для сброса пароля: {reset_link}',
                    'admin@example.com',
                    [email],
                    fail_silently=False,
                )

                notification_text = 'На ваш адрес электронной почты отправлено письмо с инструкциями по сбросу пароля'
                return render(request, self.template_name, {'reset_form': ResetForm(), 'notification': {'func': 'notifySuccess', 'text': notification_text}})
            except User.DoesNotExist:
                notification_text = 'Пользователь с данным адресом электронной почты не найден'
                return render(request, self.template_name, {'reset_form': ResetForm(), 'notification': {'func': 'notifyError', 'text': notification_text}})

        notification_text = 'Введены некорректные данные'
        return render(request, self.template_name, {'reset_form': ResetForm(), 'notification': {'func': 'notifyError', 'text': notification_text}})


class ResetConfirmView(View):
    template_name = 'users/reset-confirm.html'

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


class SettingsView(View):
    template_name = 'users/settings.html'

    @check_if_user_is_not_authorized
    def get(self, request, *args, **kwargs):
        return self.handle_request(request)

    @check_if_user_is_not_authorized
    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=request.session['user_id'])
        operation = request.POST.get('operation')

        if operation == 'turn_on_tfa':
            tfa_code = request.POST.get('tfa_code')
            code = request.POST.get('code')

            if self.is_six_digits(code) and pyotp.TOTP(tfa_code).verify(code):
                user.tfa_key = tfa_code
                user.save()

                notification_text = 'Двухфакторная аутентификация успешно подключена'
                return self.handle_request(request, notification={'func': 'notifySuccess', 'text': notification_text})
            else:
                notification_text = 'Введен неверный код'
                return self.handle_request(request, notification={'func': 'notifyError', 'text': notification_text})
        elif operation == 'turn_off_tfa':
            code = str(request.POST.get('code', ''))

            if self.is_six_digits(code) and pyotp.TOTP(user.tfa_key).verify(code):
                user.tfa_key = None
                user.save()

                notification_text = 'Двухфакторная аутентификация успешно отключена'
                return self.handle_request(request, notification={'func': 'notifySuccess', 'text': notification_text})
            else:
                notification_text = 'Введен неверный код'
                return self.handle_request(request, notification={'func': 'notifyError', 'text': notification_text})
        elif operation == 'change_session_duration':
            session_duration = request.POST.get('session_duration')

            if session_duration.isdigit() and 5 <= int(session_duration) <= 120:
                user.session_duration = int(session_duration)
                user.save()

                notification_text = 'Время сессии успешно изменено'
                return self.handle_request(request, notification={'func': 'notifySuccess', 'text': notification_text})
            else:
                notification_text = 'Выберите корректное значение'
                return self.handle_request(request, notification={'func': 'notifyError', 'text': notification_text})

        return redirect(reverse('users:settings'))

    def handle_request(self, request, **kwargs):
        user = User.objects.get(id=request.session['user_id'])
        context = {'user': user, 'notification': kwargs.get('notification')}

        if user.tfa_key is None:
            secret_key = pyotp.random_base32()
            uri = pyotp.totp.TOTP(secret_key).provisioning_uri(name=user.email, issuer_name='SafeVault')

            img = qrcode.make(uri)
            img_io = BytesIO()
            img.save(img_io, format='PNG')
            img_io.seek(0)

            tfa_qrcode = base64.b64encode(img_io.getvalue()).decode()
            context.update({'tfa_qrcode': tfa_qrcode, 'tfa_key': secret_key})

        return render(request, self.template_name, context)

    def is_six_digits(self, s):
        return bool(re.match(r'^\d{6}$', s))
