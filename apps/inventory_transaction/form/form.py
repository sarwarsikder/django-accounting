# apps/inventory_transaction/forms.py
from django import forms

from apps.accounts.models import Account
from apps.inventory.models import Inventory
from apps.inventory_transaction.models import InventoryTransaction
from apps.journal.models import Document
from apps.persons.models import Person


class InventoryTransactionForm(forms.ModelForm):
    class Meta:
        model = InventoryTransaction
        fields = ['doc_id', 'inventory', 'customer', 'unit', 'price', 'total_price', 'discount', 'expense_type',
                  'vehicle', 'note', 'date']

    def __init__(self, user_company_id, user_company_branch, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes to each form field
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        # Add specific Bootstrap classes or customization for certain fields
        self.fields['date'].widget.attrs['class'] = 'form-control datepicker'
        # Add more fields as needed

        # Reduce the size of 'note' field
        self.fields['note'].widget.attrs['cols'] = 3  # Adjust the width as needed
        self.fields['note'].widget.attrs['rows'] = 4  # Adjust the height as needed

        # Populate choices for accountID from the database
        document = Document.objects.filter(
            company_id=user_company_id,
            company_branch=user_company_branch
        )
        self.fields['doc_id'].queryset = document

        customers = Person.objects.filter(
            person_type="customer",
            active="yes",
            company_id=user_company_id,
            company_branch=user_company_branch
        )

        self.fields['customer'].queryset = customers

        inventory = Inventory.objects.filter(
            company_id=user_company_id,
            company_branch=user_company_branch
        )
        self.fields['inventory'].queryset = inventory
