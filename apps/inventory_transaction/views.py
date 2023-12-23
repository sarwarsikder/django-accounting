# apps/inventory_transaction/views.py
from django.shortcuts import render, get_object_or_404, redirect

from accounting.authentication_decorators import authentication_required
from .form.form import InventoryTransactionForm
from .models import InventoryTransaction


@authentication_required
def inventory_transaction_list(request, type_of_transaction):
    user = request.user

    user_company_id = user.company
    user_company_branch = user.company_branch
    transactions = InventoryTransaction.objects.filter(
        company_id=user.company,
        company_branch=user.company_branch,
        status=type_of_transaction
    )

    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'company': user_company_id,
        'company_branch': user_company_branch,
        'transactions': transactions,
        'type_of_transaction': type_of_transaction
    }

    return render(request, 'inventory_transaction/inventory_transaction_list.html', {'context': context})


@authentication_required
def inventory_transaction_create(request, type_of_transaction):
    user = request.user

    user_company_id = user.company
    user_company_branch = user.company_branch

    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'company': user_company_id,
        'company_branch': user_company_branch,
        'type_of_transaction': type_of_transaction,
    }

    if request.method == 'POST':
        form = InventoryTransactionForm(user_company_id, user_company_branch, request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.company_id = user_company_id
            transaction.company_branch = user_company_branch
            transaction.status = type_of_transaction
            transaction.created_by = request.user
            transaction.updated_by = request.user
            transaction.save()
            return redirect('inventory-transaction-list', type_of_transaction)
    else:
        form = InventoryTransactionForm(user_company_id, user_company_branch)
    return render(request, 'inventory_transaction/inventory_transaction_form.html', {'form': form, 'context': context})


@authentication_required
def inventory_transaction_update(request, pk, type_of_transaction):
    user = request.user

    user_company_id = user.company
    user_company_branch = user.company_branch

    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'company': user_company_id,
        'company_branch': user_company_branch,
        'type_of_transaction': type_of_transaction,
    }
    transaction = get_object_or_404(InventoryTransaction, pk=pk)
    if request.method == 'POST':
        form = InventoryTransactionForm(user_company_id, user_company_branch, request.POST, instance=transaction)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.company_id = user_company_id
            transaction.company_branch = user_company_branch
            transaction.created_by = request.user
            transaction.updated_by = request.user
            transaction.save()
            return redirect('inventory-transaction-list', type_of_transaction)
    else:
        form = InventoryTransactionForm(user_company_id, user_company_branch, instance=transaction)
    return render(request, 'inventory_transaction/inventory_transaction_form.html', {'form': form, 'context': context})


@authentication_required
def inventory_transaction_delete(request, pk):
    transaction = get_object_or_404(InventoryTransaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        return redirect('inventory-transaction-list')
    return render(request, 'inventory_transaction/inventory_transaction_confirm_delete.html',
                  {'transaction': transaction})
