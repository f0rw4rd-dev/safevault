from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.views.generic import View
from users.decorators import check_if_user_is_not_authorized


class ListView(View):
    template_name = 'passwords/passwords.html'

    @check_if_user_is_not_authorized
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
