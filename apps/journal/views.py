# views.py
import json
from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect

from accounting.authentication_decorators import authentication_required
from .forms.forms import TransactionForm, DocumentForm
from .models import Transaction, Document
from ..accounts.models import Account
from ..persons.models import Person


@authentication_required
def transaction_list(request):
    user = request.user
    user_company_id = user.company
    user_company_branch = user.company_branch
    transactions = Transaction.objects.filter(company_id=user_company_id, company_branch=user_company_branch)
    documents = Document.objects.filter(company_id=user_company_id, company_branch=user_company_branch)

    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'company': user_company_id,
        'company_branch': user_company_branch,
        'transactions': transactions,
        'documents': documents
    }

    return render(request, 'journal/transaction_list.html', {'context': context})


@authentication_required
def create_transaction(request):
    user = request.user
    user_company_id = user.company
    user_company_branch = user.company_branch

    accounts = Account.objects.filter(
        company_id=user_company_id,
        company_branch=user_company_branch
    )

    customers = Person.objects.filter(
        person_type="customer",
        active="yes",
        company_id=user_company_id,
        company_branch=user_company_branch
    )

    suppliers = Person.objects.filter(
        person_type="supplier",
        active="yes",
        company_id=user_company_id,
        company_branch=user_company_branch
    )

    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'company': user_company_id,
        'company_branch': user_company_branch,
        'accounts': json.dumps([{'id': account.accountID, 'name': account.name} for account in accounts]),
        'customers': json.dumps([{'id': customer.personsID, 'name': customer.persons_name} for customer in customers]),
        'suppliers': json.dumps([{'id': supplier.personsID, 'name': supplier.persons_name} for supplier in suppliers]),
    }

    print(request.POST)

    if request.method == 'POST':
        form = DocumentForm(user_company_id, user_company_branch, request.POST)

        print(request.method)

        account_list = request.POST.getlist('account[]')
        customer_list = request.POST.getlist('customer[]')
        debit_list = request.POST.getlist('debit[]')
        credit_list = request.POST.getlist('credit[]')
        description_list = request.POST.getlist('description[]')

        if form.is_valid():
            document = form.save(commit=False)
            document.company_id = user_company_id
            document.company_branch = user_company_branch
            document.created_by = request.user
            document.updated_by = request.user
            document.save()

            # Create and save Transaction objects
            for account, customer, debit, credit, description in zip(account_list, customer_list, debit_list,
                                                                     credit_list, description_list):
                account = Account.objects.get(
                    company_id=user_company_id,
                    company_branch=user_company_branch,
                    accountID=account
                )

                customer = Person.objects.get(
                    company_id=user_company_id,
                    company_branch=user_company_branch,
                    personsID=customer
                )

                Transaction.objects.create(
                    doc_id=document,
                    account=account,
                    customer=customer,
                    company_id=user_company_id,
                    company_branch=user_company_branch,
                    debit=debit,
                    credit=credit,
                    date=datetime.now(),
                    created_by=request.user,
                    updated_by=request.user,
                )

            return redirect('transaction-list')

    else:
        form = DocumentForm(user_company_id, user_company_branch, )

    # if request.method == 'POST':
    #     form = TransactionForm(user_company_id, user_company_branch, request.POST)
    #     if form.is_valid():
    #         transaction = form.save(commit=False)
    #         transaction.created_by = request.user
    #         transaction.updated_by = request.user
    #         transaction.company_id = user_company_id
    #         transaction.company_branch = user_company_branch
    #         transaction.save()
    #         return redirect('transaction-list')
    # else:
    #     form = TransactionForm(user_company_id=user_company_id, user_company_branch=user_company_branch)
    return render(request, 'journal/create_transaction.html', {'form': form, 'context': context})


@authentication_required
def update_transaction(request, doc_id):
    user = request.user
    user_company_id = user.company
    user_company_branch = user.company_branch

    document = get_object_or_404(
        Document,
        doc_id=doc_id
    )

    print(doc_id)
    print(document.doc_id)

    accounts = Account.objects.filter(
        company_id=user_company_id,
        company_branch=user_company_branch
    )

    transactions = Transaction.objects.filter(
        doc_id=document.doc_id
    )

    customers = Person.objects.filter(
        person_type="customer",
        active="yes",
        company_id=user_company_id,
        company_branch=user_company_branch
    )

    suppliers = Person.objects.filter(
        person_type="supplier",
        active="yes",
        company_id=user_company_id,
        company_branch=user_company_branch
    )

    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'company': user_company_id,
        'company_branch': user_company_branch,
        'accounts': json.dumps([{'id': account.accountID, 'name': account.name} for account in accounts]),
        'customers': json.dumps([{'id': customer.personsID, 'name': customer.persons_name} for customer in customers]),
        'suppliers': json.dumps([{'id': supplier.personsID, 'name': supplier.persons_name} for supplier in suppliers]),
        'transactions': transactions,  # Note the plural form
        'document': document,  # Note the plural form
    }

    if request.method == 'POST':
        form = DocumentForm(user_company_id, user_company_branch, request.POST, instance=document)
        if form.is_valid():
            document = form.save(commit=False)
            document.updated_by = request.user
            document.save()

            for index, transaction_item in enumerate(transactions):
                account = Account.objects.get(
                    company_id=user_company_id,
                    company_branch=user_company_branch,
                    accountID=request.POST.get(f'account_{index}')
                )

                customer = Person.objects.get(
                    company_id=user_company_id,
                    company_branch=user_company_branch,
                    personsID=request.POST.get(f'customer_{index}')
                )

                transaction_item.account = account
                transaction_item.customer = customer
                transaction_item.debit = request.POST.get(f'debit_{index}')
                transaction_item.credit = request.POST.get(f'credit_{index}')
                transaction_item.description = request.POST.get(f'description_{index}')
                transaction_item.save()

            return redirect('transaction-list')

    else:
        print(transactions)
        print("TEST")
        form = DocumentForm(user_company_id, user_company_branch, instance=document)
        print("TEST")

    return render(request, 'journal/update_transaction.html', {'form': form, 'context': context})


@authentication_required
def delete_transaction(request, doc_id):
    user = request.user
    documents = get_object_or_404(Document, pk=doc_id)
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'company': user.company,
        'company_branch': user.company_branch_id,
    }

    if request.method == 'POST':
        documents.delete()

        return redirect('asset-list')
    return render(request, 'journal/transaction_confirm_delete.html', {'transaction': documents, 'context': context})
