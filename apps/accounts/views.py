from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from accounting.authentication_decorators import authentication_required
from apps.accounts.forms.accounting_forms import AccountForm, AccountFormEdit
from apps.accounts.models import AccountLevel2, AccountLevel3, Account


@authentication_required
def index(request):
    user = request.user
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'company': user.company,
        'company_branch': user.company_branch,
    }
    return render(request, 'dashboard/index.html', {'context': context})


@authentication_required
def account_list(request):
    user = request.user
    accounts = Account.objects.filter(company_id=user.company, company_branch=user.company_branch)

    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'company': user.company,
        'company_branch': user.company_branch,
        'accounts': accounts,
    }

    return render(request, 'accounts/account_list.html', {'context': context})


@authentication_required
def account_create(request):
    user = request.user
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'company': user.company,
        'company_branch': user.company_branch,
    }

    if request.method == 'POST':
        print(request.POST)
        form = AccountForm(request.POST)
        if form.is_valid():
            user = request.user
            account = form.save(commit=False)
            account.company_id = user.company
            account.company_branch = user.company_branch
            account.created_by = user
            account.updated_by = user
            account.level3ID = form.cleaned_data['level3']
            account.level2ID = form.cleaned_data['level2']
            account.level1ID = form.cleaned_data['level1']
            account.save()
            return redirect('account-list')
    else:
        form = AccountForm()

    return render(request, 'accounts/account_form.html', {'form': form, 'context': context})


@authentication_required
def edit_account(request, account_id):
    user = request.user
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'company': user.company,
        'company_branch': user.company_branch,
    }
    account = get_object_or_404(Account, accountID=account_id, company_id=user.company,
                                company_branch=user.company_branch)
    if request.method == 'POST':
        form = AccountFormEdit(request.POST, instance=account)
        if form.is_valid():
            user = request.user
            account = form.save(commit=False)
            account.company_id = user.company
            account.company_branch = user.company_branch
            account.created_by = user
            account.updated_by = user
            # Access cleaned data dictionary
            cleaned_data = form.cleaned_data

            # Check if the keys are present in the cleaned data
            account.level3ID = cleaned_data['level3ID']
            account.level2ID = cleaned_data['level2ID']
            account.level1ID = cleaned_data['level1ID']

            account.save()

            return redirect('account-list')
    else:
        form = AccountFormEdit(instance=account)
    # Your view logic here...
    return render(request, 'accounts/edit_account.html', {'form': form, 'account_id': account_id, 'context': context})


@authentication_required
def delete_account(request, account_id):
    user = request.user
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'company': user.company,
        'company_branch': user.company_branch,
    }
    account = get_object_or_404(Account, pk=account_id)

    if request.method == 'POST':
        account.delete()
        return redirect('account-list')
    # Your view logic here...
    return render(request, 'accounts/delete_account.html',
                  {'account_id': account_id, 'context': context})


def get_account_level2_options(request):
    level1_id = request.GET.get('level1ID')
    print("TEST" + level1_id)
    level2_options = AccountLevel2.objects.filter(level1ID=level1_id).values('level2ID', 'name')

    print(level2_options)
    # Perform a database query or any other logic to get the options
    # ...

    # Return the options as JSON
    data = [{'level2ID': option['level2ID'], 'name': option['name']} for option in level2_options]

    print(data)
    return JsonResponse(data, safe=False)


def get_account_level3_options(request):
    level2_id = request.GET.get('level2ID')
    level3_options = AccountLevel3.objects.filter(level2ID=level2_id).values('level3ID', 'name')
    data = [{'level3ID': option['level3ID'], 'name': option['name']} for option in level3_options]
    return JsonResponse(data, safe=False)
