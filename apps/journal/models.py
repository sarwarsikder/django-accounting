from django.db import models

from accounting import settings
from apps.accounts.models import Account
from apps.company.models import Company, CompanyBranch
from apps.persons.models import Person


class Document(models.Model):
    # Fields
    doc_id = models.AutoField(primary_key=True)
    date = models.DateField()
    notes = models.TextField()
    name = models.CharField(null=True, blank=True, max_length=150)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    company_branch = models.ForeignKey(CompanyBranch, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='created_docs', null=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='updated_docs', null=True)

    def __str__(self):
        return f"{self.doc_id} - {self.name}"


class Transaction(models.Model):
    # Fields
    transaction_id = models.AutoField(primary_key=True)
    doc_id = models.ForeignKey(Document, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    customer = models.ForeignKey(Person, on_delete=models.CASCADE)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    company_branch = models.ForeignKey(CompanyBranch, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    debit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='created_transactions')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='updated_transactions')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.transaction_id} - {self.doc_id} - {self.account} - {self.customer} - {self.date} - {self.debit} - {self.credit} - {self.notes}"
