from django.shortcuts import redirect, reverse


def check_if_user_is_authorized(func):
    def wrapper(self, request, *args, **kwargs):
        if request.session.get('user_id'):
            return redirect(reverse('passwords:list'))

        return func(self, request, *args, **kwargs)

    return wrapper


def check_if_user_is_not_authorized(func):
    def wrapper(self, request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect(reverse('users:login'))

        return func(self, request, *args, **kwargs)

    return wrapper
