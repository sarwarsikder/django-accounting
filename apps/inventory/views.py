from django.shortcuts import render, redirect, get_object_or_404

from accounting.authentication_decorators import authentication_required
from .forms.forms import InventoryForm, InventoryFormEdit
from .models import Inventory


@authentication_required
def inventory_list(request):
    user = request.user
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'company': user.company,
        'company_branch': user.company_branch_id,
        'inventory_list': Inventory.objects.filter(company_id=user.company, company_branch=user.company_branch)

    }

    return render(request, 'inventory/inventory_list.html', {'context': context})


@authentication_required
def inventory_create(request):
    user = request.user
    user_company_id = user.company
    user_company_branch = user.company_branch
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'company': user_company_id,
        'company_branch': user_company_branch,
    }
    if request.method == 'POST':
        form = InventoryForm(user_company_id, user_company_branch, request.POST)
        if form.is_valid():
            user = request.user
            inventory = form.save(commit=False)
            inventory.company_id = user.company
            inventory.company_branch = user.company_branch
            inventory.account = form.cleaned_data['account']
            inventory.save()
            return redirect('inventory-list')
    else:
        form = InventoryForm(user_company_id, user_company_branch)
    return render(request, 'inventory/inventory_form.html', {'form': form, 'context': context})


@authentication_required
def inventory_update(request, pk):
    user = request.user
    user_company_id = user.company
    user_company_branch = user.company_branch
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'company': user_company_id,
        'company_branch': user_company_branch,
    }
    inventory = get_object_or_404(Inventory, pk=pk)

    if request.method == 'POST':
        form = InventoryFormEdit(user_company_id, user_company_branch, data=request.POST, instance=inventory)
        if form.is_valid():
            inventory = form.save(commit=False)
            inventory.company_id = user_company_id
            inventory.company_branch = user_company_branch
            inventory.account = form.cleaned_data['account']
            inventory.save()
            return redirect('inventory-list')
    else:
        form = InventoryFormEdit(user_company_id, user_company_branch, instance=inventory)

    return render(request, 'inventory/inventory_form.html', {'form': form, 'context': context})


@authentication_required
def inventory_delete(request, pk):
    user = request.user
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'company': user.company,
        'company_branch': user.company_branch_id,
    }
    inventory = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        inventory.delete()
        return redirect('inventory-list')

    return render(request, 'inventory/inventory_confirm_delete.html', {'inventory': inventory, 'context': context})
