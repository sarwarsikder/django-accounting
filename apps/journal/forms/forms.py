from django import forms

from apps.accounts.models import Account
from apps.journal.models import Transaction, Document
from apps.persons.models import Person


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'notes', 'date']

    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        # You can customize the form fields if needed
        self.fields['date'].widget.attrs.update({'class': 'datepicker form-control', 'placeholder': 'Select a date'})
        self.fields['notes'].widget.attrs.update({'class': 'form-control', 'rows': '3', 'placeholder': 'Enter notes'})
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter name'})


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['doc_id', 'account', 'customer', 'date', 'debit', 'credit', 'notes']

    def __init__(self, user_company_id, user_company_branch, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes to each form field
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        # Add specific Bootstrap classes or customization for certain fields
        self.fields['date'].widget.attrs['class'] = 'form-control datepicker'
        # Add more fields as needed

        # Reduce the size of 'notes' field
        self.fields['notes'].widget.attrs['cols'] = 3  # Adjust the width as needed
        self.fields['notes'].widget.attrs['rows'] = 4  # Adjust the height as needed

        accounts = Account.objects.filter(
            company_id=user_company_id,
            company_branch=user_company_branch
        )
        self.fields['account'].queryset = accounts

        customers = Person.objects.filter(
            person_type="customer",
            active="yes",
            company_id=user_company_id,
            company_branch=user_company_branch
        )

        self.fields['customer'].queryset = customers
