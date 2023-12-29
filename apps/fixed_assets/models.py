from django.db import models
from accounting import settings

from apps.accounts.models import Account

from django.db import models

from apps.company.models import Company, CompanyBranch


class DepreciationCategory(models.Model):
    accu_id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=255)
    year = models.IntegerField()
    year_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.accu_id}"


class FixedAsset(models.Model):
    # Choices for the depreciation field
    YES = 'yes'
    NO = 'no'
    DEPRECIATION_CHOICES = [
        (NO, 'No'),
        (YES, 'Yes'),
    ]
    # Relationships
    depreciation_id = models.CharField(primary_key=True, max_length=10, unique=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    accu_id = models.ForeignKey(DepreciationCategory, on_delete=models.CASCADE, null=True)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, default=None)
    company_branch = models.ForeignKey(CompanyBranch, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Example decimal field
    purchase_month = models.DateField()
    depreciation = models.CharField(max_length=3, choices=DEPRECIATION_CHOICES, default=NO)
    identification = models.CharField(max_length=255)
    details = models.TextField()
    notes = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_assets', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='updated_assets', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DepreciationProcess(models.Model):
    depreciation_process_id = models.AutoField(primary_key=True)
    depreciation_id = models.OneToOneField(FixedAsset, on_delete=models.CASCADE, null=True)
    depreciation_amount = models.DecimalField(max_digits=10, decimal_places=2)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.depreciation_process_id} - {self.year} - {self.depreciation_id} - {self.depreciation_amount}"
