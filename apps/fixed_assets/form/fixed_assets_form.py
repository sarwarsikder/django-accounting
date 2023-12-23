from django import forms

from apps.accounts.models import Account
from apps.fixed_assets.models import FixedAsset, DepreciationCategory


class FixedAssetForm(forms.ModelForm):
    class Meta:
        model = FixedAsset
        fields = ['account', 'accu_id', 'name', 'type', 'brand', 'price',
                  'purchase_month', 'depreciation', 'identification', 'details', 'notes']

        widgets = {
            'purchase_month': forms.DateInput(attrs={'class': 'form-control datepicker'}),
        }

    def __init__(self, user_company_id, user_company_branch, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes to each form field
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        # Populate choices for accountID from the database
        accounts = Account.objects.filter(
            company_id=user_company_id,
            company_branch=user_company_branch
        )
        self.fields['account'].queryset = accounts

        # Populate choices for accu_id from the database
        depreciation_categories = DepreciationCategory.objects.all()
        self.fields['accu_id'].queryset = depreciation_categories

        # Add specific Bootstrap classes or customization for certain fields
        self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['depreciation'].widget.attrs['class'] = 'form-control'
        self.fields['purchase_month'].widget.attrs['class'] = 'form-control datepicker'

        # Reduce the size of 'details' and 'note' fields
        self.fields['details'].widget.attrs['cols'] = 3  # Adjust the width as needed
        self.fields['details'].widget.attrs['rows'] = 4  # Adjust the width as needed
        self.fields['notes'].widget.attrs['cols'] = 3  # Adjust the width as needed
        self.fields['notes'].widget.attrs['rows'] = 4  # Adjust the width as needed
