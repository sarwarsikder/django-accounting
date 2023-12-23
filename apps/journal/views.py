# views.py
from django.shortcuts import render, get_object_or_404, redirect

from accounting.authentication_decorators import authentication_required
from .forms.forms import TransactionForm
from .models import Transaction


@authentication_required
def transaction_list(request):
    user = request.user
    user_company_id = user.company
    user_company_branch = user.company_branch
    transactions = Transaction.objects.filter(company_id=user_company_id, company_branch=user_company_branch)

    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'company': user_company_id,
        'company_branch': user_company_branch,
        'transactions': transactions
    }

    return render(request, 'journal/transaction_list.html', {'context': context})


@authentication_required
def create_transaction(request):
    user = request.user
    user_company_id = user.company
    user_company_branch = user.company_branch

    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'company': user_company_id,
        'company_branch': user_company_branch
    }

    if request.method == 'POST':
        form = TransactionForm(user_company_id, user_company_branch, request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.created_by = request.user
            transaction.updated_by = request.user
            transaction.company_id = user_company_id
            transaction.company_branch = user_company_branch
            transaction.save()
            return redirect('transaction-list')
    else:
        form = TransactionForm(user_company_id=user_company_id, user_company_branch=user_company_branch)
    return render(request, 'journal/create_transaction.html', {'form': form, 'context': context})


@authentication_required
def update_transaction(request, transaction_id):
    user = request.user
    user_company_id = user.company
    user_company_branch = user.company_branch
    transaction = get_object_or_404(Transaction, pk=transaction_id)

    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'company': user_company_id,
        'company_branch': user_company_branch,
        'transaction': transaction
    }

    if request.method == 'POST':
        form = TransactionForm(user_company_id, user_company_branch, request.POST, instance=transaction)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.company_id = user_company_id
            transaction.company_branch = user_company_branch
            transaction.updated_by = request.user
            transaction.save()
            return redirect('transaction-list')
    else:
        form = TransactionForm(user_company_id=user_company_id, user_company_branch=user_company_branch,
                               instance=transaction)
    return render(request, 'journal/update_transaction.html', {'form': form, 'transaction': transaction})


@authentication_required
def delete_transaction(request, transaction_id):
    user = request.user
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'company': user.company,
        'company_branch': user.company_branch_id,
    }

    if request.method == 'POST':
        transaction.delete()

        return redirect('asset-list')
    return render(request, 'journal/transaction_confirm_delete.html', {'transaction': transaction, 'context': context})
