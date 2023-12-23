# views.py
from django.shortcuts import render, get_object_or_404, redirect

from accounting.authentication_decorators import authentication_required
from .form.fixed_assets_form import FixedAssetForm
from .models import FixedAsset


@authentication_required
def asset_list(request):
    user = request.user

    fixed_assets = FixedAsset.objects.filter(company_id=user.company, company_branch=user.company_branch)

    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'company': user.company,
        'company_branch': user.company_branch,
        'fixed_assets': fixed_assets,
    }
    return render(request, 'fixed_assets/asset_list.html', {'context': context})


@authentication_required
def create_asset(request):
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
        form = FixedAssetForm(user_company_id, user_company_branch, request.POST)
        if form.is_valid():
            user = request.user

            fixed_asset_instance = form.save(commit=False)
            fixed_asset_instance.company_id = user_company_id
            fixed_asset_instance.company_branch = user_company_branch
            fixed_asset_instance.created_by_id = user.id
            fixed_asset_instance.updated_by_id = user.id
            fixed_asset_instance.save()

            return redirect('asset-list')
    else:
        form = FixedAssetForm(user_company_id=user_company_id, user_company_branch=user_company_branch)

    return render(request, 'fixed_assets/create_asset.html', {'context': context, 'form': form})


@authentication_required
def update_asset(request, depreciation_id):
    user = request.user
    user_company_id = user.company
    user_company_branch = user.company_branch
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'company': user_company_id,
        'company_branch': user_company_branch,
    }
    asset = get_object_or_404(FixedAsset, depreciation_id=depreciation_id)
    if request.method == 'POST':
        form = FixedAssetForm(user_company_id, user_company_branch, request.POST, instance=asset)
        if form.is_valid():
            cleaned_data = form.cleaned_data

            form = form.save(commit=False)
            form.company_id = user.company
            form.company_branch = user.company_branch
            form.account = cleaned_data['account']
            form.accu_id = cleaned_data['accu_id']
            form.save()
            return redirect('asset-list')
    else:
        form = FixedAssetForm(user_company_id=user_company_id, user_company_branch=user_company_branch, instance=asset)
    return render(request, 'fixed_assets/update_asset.html', {'context': context, 'form': form, 'asset': asset})


@authentication_required
def delete_asset(request, depreciation_id):
    user = request.user
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'company': user.company,
        'company_branch': user.company_branch_id,
    }
    asset = get_object_or_404(FixedAsset, depreciation_id=depreciation_id)

    if request.method == 'POST':
        asset.delete()

        return redirect('asset-list')
    return render(request, 'fixed_assets/asset_confirm_delete.html', {'asset': asset, 'context': context})
