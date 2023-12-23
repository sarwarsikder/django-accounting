# accounts/views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404

from .models import CustomUser

from accounting.authentication_decorators import is_authorized, authentication_required
from .form.login_form import LoginForm


@is_authorized
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                # Redirect to the dashboard or any other page
                return redirect('/')
            else:
                # Handle invalid login credentials
                pass
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'form': form})


@authentication_required
def user_list(request):
    user = request.user
    if user.company and user.company_branch:
        qs = CustomUser.objects.filter(company=user.company, company_branch=user.company_branch)
    else:
        # If user's company or company branch is not set, return an empty queryset
        qs = CustomUser.objects.none()
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'company': user.company,
        'company_branch': user.company_branch,
        'branch_users': qs
    }
    return render(request, 'users/index.html', context)


@authentication_required
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')  # Redirect to user list page after editing
    else:
        form = EditUserForm(instance=user)

    context = {
        'form': form,
        'user_id': user_id,
    }
    return render(request, 'users/edit_user.html', context)


@authentication_required
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')  # Redirect to user list page after deleting

    context = {
        'user': user,
    }
    return render(request, 'users/delete_user.html', context)
