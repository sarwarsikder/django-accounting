# apps/inventory_transaction/views.py
from django.shortcuts import render, get_object_or_404, redirect

from accounting.authentication_decorators import authentication_required
from .form.form import InventoryTransactionForm
from .models import InventoryTransaction
from ..inventory.models import Inventory
from ..journal.models import Document, Transaction
from ..persons.models import Person


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
            document = Document()
            document.notes = request.POST['note']
            document.date = request.POST['date']
            document.company_id = user_company_id
            document.company_branch = user_company_branch
            document.created_by = request.user
            document.updated_by = request.user
            document.save()

            total_price = float(int(request.POST['unit']) * float(request.POST['price'])) - float(
                request.POST['discount'])

            inventory_transaction = form.save(commit=False)
            inventory_transaction.doc_id = document
            inventory_transaction.company_id = user_company_id
            inventory_transaction.company_branch = user_company_branch
            inventory_transaction.status = type_of_transaction
            inventory_transaction.total_price = total_price
            inventory_transaction.created_by = request.user
            inventory_transaction.updated_by = request.user
            inventory_transaction.save()

            inventory = Inventory.objects.get(
                inventoryID=request.POST['inventory']
            )

            person = Person.objects.get(
                personsID=request.POST['supplier']
            )

            Transaction.objects.create(
                doc_id=document,
                account=inventory.account,
                customer=person,
                company_id=user_company_id,
                company_branch=user_company_branch,
                debit=0.00,
                credit=total_price,
                date=request.POST['date'],
                created_by=request.user,
                updated_by=request.user,
            )

            Transaction.objects.create(
                doc_id=document,
                account=inventory.account,
                company_id=user_company_id,
                company_branch=user_company_branch,
                debit=total_price,
                credit=0.00,
                date=request.POST['date'],
                created_by=request.user,
                updated_by=request.user,
            )

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

            print(transaction.doc_id.doc_id)

            document = Document.objects.get(
                doc_id=transaction.doc_id.doc_id
            )

            print("TEST")

            document.notes = request.POST['note']
            document.date = request.POST['date']
            document.updated_by = request.user
            document.save()


            total_price = float(int(request.POST['unit']) * float(request.POST['price'])) - float(
                request.POST['discount'])

            inventory = Inventory.objects.get(
                inventoryID=request.POST['inventory']
            )

            person = Person.objects.get(
                personsID=request.POST['supplier']
            )

            Transaction.objects.filter(doc_id=document).delete()

            Transaction.objects.create(
                doc_id=document,
                account=inventory.account,
                customer=person,
                company_id=user_company_id,
                company_branch=user_company_branch,
                debit=0.00,
                credit=total_price,
                date=request.POST['date'],
                created_by=request.user,
                updated_by=request.user,
            )

            Transaction.objects.create(
                doc_id=document,
                account=inventory.account,
                company_id=user_company_id,
                company_branch=user_company_branch,
                debit=total_price,
                credit=0.00,
                date=request.POST['date'],
                created_by=request.user,
                updated_by=request.user,
            )

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
