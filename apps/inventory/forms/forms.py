from django import forms

from apps.accounts.models import Account
from apps.inventory.models import Inventory, Measures
from apps.persons.models import Person  # Assuming your persons model is in the 'persons' app


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['account', 'measure', 'inventory_item_name', 'inventory_type', 'avg_price', 'detail',
                  'note']

    def __init__(self, user_company_id, user_company_branch, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes to each form field
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        # Add specific Bootstrap classes or customization for certain fields
        self.fields['avg_price'].widget.attrs['class'] = 'form-control'  # Example for avg_price field

        # Filter choices for supplierID based on criteria (person_type, company_id, company_branch)
        suppliers = Person.objects.filter(
            person_type='supplier',
            company_id=user_company_id,
            company_branch=user_company_branch,
            active='yes'

        )
        # self.fields['supplierID'].queryset = suppliers

        # Reduce the size of 'details' and 'note' fields
        self.fields['detail'].widget.attrs['cols'] = 3  # Adjust the width as needed
        self.fields['detail'].widget.attrs['rows'] = 4  # Adjust the width as needed
        self.fields['note'].widget.attrs['cols'] = 3  # Adjust the width as needed
        self.fields['note'].widget.attrs['rows'] = 4  # Adjust the width as needed

    # def clean_supplierID(self):
    #     # Optional: You can add additional validation for the supplierID field if needed
    #     supplier_id = self.cleaned_data['supplierID']
    #     # Your validation logic here
    #     return supplier_id


class InventoryFormEdit(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['account', 'measure', 'inventory_item_name', 'inventory_type', 'avg_price', 'detail',
                  'note']

    def __init__(self, user_company_id, user_company_branch, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes to each form field
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        # Add specific Bootstrap classes or customization for certain fields
        self.fields['avg_price'].widget.attrs['class'] = 'form-control'  # Example for avg_price field

        # Filter choices for supplierID based on criteria (person_type, company_id, company_branch)
        suppliers = Person.objects.filter(
            person_type='supplier',
            company_id=user_company_id,
            company_branch=user_company_branch
        )
        # self.fields['supplierID'].queryset = suppliers

        # Populate choices for accountID from the database
        accounts = Account.objects.filter(
            company_id=user_company_id,
            company_branch=user_company_branch
        )
        self.fields['account'].queryset = accounts

        # Populate choices for measure from the database
        measures = Measures.objects.all()
        self.fields['measure'].queryset = measures

        # Pre-select the dropdown values if the instance exists
        if self.instance:
            self.fields['account'].initial = self.instance.account
            # self.fields['supplierID'].initial = self.instance.supplierID
            self.fields['measure'].initial = self.instance.measure

        self.fields['detail'].widget.attrs['cols'] = 3  # Adjust the width as needed
        self.fields['detail'].widget.attrs['rows'] = 4  # Adjust the width as needed
        self.fields['note'].widget.attrs['cols'] = 3  # Adjust the width as needed
        self.fields['note'].widget.attrs['rows'] = 4  # Adjust the width as needed

    # def clean_supplierID(self):
    #     # Optional: You can add additional validation for the supplierID field if needed
    #     supplier_id = self.cleaned_data['supplierID']
    #     # Your validation logic here
    #     return supplier_id
