from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from .models import User
from .forms import LoginForm, RegisterForm

import os
import binascii


class LoginView(View):
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    # def post(self, request, *args, **kwargs):
    #     email = request.POST.get('email')
    #     master_password = request.POST.get('master_password')
    #     user = User.objects.filter(email=email, master_password=master_password).first()
    #     if user:
    #         return render(request, self.template_name, {'message': 'Login successful'})
    #     return render(request, self.template_name, {'message': 'Login failed'})


class RegisterView(View):
    template_name = 'users/register.html'

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})


class ResetView(View):
    template_name = 'users/reset.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class Reset2View(View):
    template_name = 'users/reset-2.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class UserAPIView(View):
    def get(self, request, *args, **kwargs):
        email = request.GET.get('email')

        if not email:
            return JsonResponse({'error': 'The "email" parameter is required'}, status=400)

        salt = binascii.hexlify(os.urandom(16)).decode()
        init_vector = binascii.hexlify(os.urandom(16)).decode()

        user = User.objects.filter(email=email).first()
        if user:
            salt = user.salt
            init_vector = user.init_vector

        return JsonResponse({'email': email, 'salt': salt, 'init_vector': init_vector})
