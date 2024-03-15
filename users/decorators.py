from django.http import HttpResponseForbidden
from django.shortcuts import redirect, reverse


def check_if_user_is_authorized(func):
    def wrapper(self, request, *args, **kwargs):
        if request.session.get('user_id'):
            return redirect(reverse('passwords:passwords'))

        return func(self, request, *args, **kwargs)

    return wrapper


def check_if_user_is_not_authorized(func):
    def wrapper(self, request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect(reverse('users:login'))

        return func(self, request, *args, **kwargs)

    return wrapper


def api_check_if_user_is_not_authorized(func):
    def wrapper(self, request, *args, **kwargs):
        if not request.session.get('user_id'):
            return HttpResponseForbidden()

        return func(self, request, *args, **kwargs)

    return wrapper
