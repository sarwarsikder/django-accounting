from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

from apps.accounts.models import Account
from apps.company.models import Company, CompanyBranch
from apps.persons.models import Person


class Measures(models.Model):
    measureID = models.AutoField(primary_key=True)
    measure = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.measure


class Inventory(models.Model):
    inventoryID = models.AutoField(primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    supplierID = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    inventory_item_name = models.CharField(max_length=255)
    inventory_type = models.CharField(max_length=255)
    measure = models.ForeignKey(Measures, on_delete=models.CASCADE)
    avg_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    detail = models.TextField()
    note = models.TextField()
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, default=None)
    company_branch = models.ForeignKey(CompanyBranch, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.inventory_item_name} - {self.account.name}"
