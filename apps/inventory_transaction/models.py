from django.db import models

from accounting import settings
from apps.accounts.models import Account
from apps.company.models import Company, CompanyBranch
from apps.inventory.models import Inventory
from apps.journal.models import Document
from apps.persons.models import Person


class InventoryTransaction(models.Model):
    PURCHASE = 'inventory-purchase'
    USE = 'inventory-use'
    RETURN_TO_INVENTORY = 'return-to-inventory'
    RETURN_TO_SUPPLIER = 'return-to-supplier'

    STATUS_CHOICES = [
        (PURCHASE, 'Inventory Purchase'),
        (USE, 'Inventory Use'),
        (RETURN_TO_INVENTORY, 'Return to Inventory'),
        (RETURN_TO_SUPPLIER, 'Return to Supplier'),
    ]

    inv_transID = models.AutoField(primary_key=True)
    doc_id = models.ForeignKey(Document, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    customer = models.ForeignKey(Person, on_delete=models.CASCADE)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, default=None)
    company_branch = models.ForeignKey(CompanyBranch, on_delete=models.CASCADE, default=None)
    unit = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    expense_type = models.CharField(max_length=100)
    vehicle = models.CharField(max_length=100)
    note = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    date = models.DateField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_inventory_transactions',
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='updated_inventory_transactions',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.inv_transID} - {self.inventory} - {self.status}"
