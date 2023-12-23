# decorators.py
from django.shortcuts import redirect


def authentication_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Replace 'login' with the name of your login URL
        return view_func(request, *args, **kwargs)

    return wrapped_view


def is_authorized(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')  # Replace 'login' with the name of your login URL
        return view_func(request, *args, **kwargs)

    return wrapped_view
