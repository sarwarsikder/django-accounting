# apps/inventory_transaction/forms.py
from django import forms

from apps.accounts.models import Account
from apps.inventory.models import Inventory
from apps.inventory_transaction.models import InventoryTransaction
from apps.persons.models import Person


class InventoryTransactionForm(forms.ModelForm):
    class Meta:
        model = InventoryTransaction
        fields = ['date', 'note', 'inventory', 'supplier', 'unit', 'price', 'discount', 'expense_type',
                  'vehicle']

    def __init__(self, user_company_id, user_company_branch, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes to each form field
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        # Add specific Bootstrap classes or customization for certain fields
        self.fields['date'].widget.attrs['class'] = 'form-control datepicker'
        # Add more fields as needed

        # Reduce the size of 'note' field
        self.fields['note'].widget.attrs['cols'] = 2  # Adjust the width as needed
        self.fields['note'].widget.attrs['rows'] = 3  # Adjust the height as needed

        suppliers = Person.objects.filter(
            person_type="supplier",
            active="yes",
            company_id=user_company_id,
            company_branch=user_company_branch
        )

        self.fields['supplier'].queryset = suppliers

        inventory = Inventory.objects.filter(
            company_id=user_company_id,
            company_branch=user_company_branch
        )

        self.fields['inventory'].queryset = inventory

        account = Account.objects.filter(
            company_id=user_company_id,
            company_branch=user_company_branch
        )

        self.fields['expense_type'].queryset = account
        self.fields['vehicle'].queryset = account


class InventoryTransactionFormRTS(forms.ModelForm):
    account = forms.ModelChoiceField(queryset=Account.objects.filter(accountID__startswith='2120'))

    class Meta:
        model = InventoryTransaction
        fields = ['date', 'note', 'account', 'inventory', 'supplier', 'unit', 'price', 'discount', 'expense_type',
                  'vehicle']

    def __init__(self, user_company_id, user_company_branch, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes to each form field
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        # Add specific Bootstrap classes or customization for certain fields
        self.fields['date'].widget.attrs['class'] = 'form-control datepicker'
        # Add more fields as needed

        # Reduce the size of 'note' field
        self.fields['note'].widget.attrs['cols'] = 2  # Adjust the width as needed
        self.fields['note'].widget.attrs['rows'] = 3  # Adjust the height as needed

        suppliers = Person.objects.filter(
            person_type="customer",
            active="yes",
            company_id=user_company_id,
            company_branch=user_company_branch
        )

        self.fields['supplier'].queryset = suppliers
        self.fields['supplier'].label = 'Customer'

        inventory = Inventory.objects.filter(
            company_id=user_company_id,
            company_branch=user_company_branch
        )

        self.fields['inventory'].queryset = inventory

        account = Account.objects.filter(
            company_id=user_company_id,
            company_branch=user_company_branch
        )

        self.fields['expense_type'].queryset = account
        self.fields['vehicle'].queryset = account
