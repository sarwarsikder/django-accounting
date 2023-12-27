from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# models.py

from django.db import models

from accounting import settings
from apps.company.models import Company, CompanyBranch


class AccountLevel1(models.Model):
    # level1ID = models.IntegerField(primary_key=True, choices=[(i, str(i)) for i in range(10)])
    level1ID = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AccountLevel2(models.Model):
    # level2ID = models.IntegerField(primary_key=True)
    level2ID = models.IntegerField(primary_key=True)
    level1ID = models.ForeignKey(AccountLevel1, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AccountLevel3(models.Model):
    # level3ID = models.IntegerField(primary_key=True, choices=[(i, str(i)) for i in range(10)])
    level3ID = models.IntegerField(primary_key=True)
    level2ID = models.ForeignKey(AccountLevel2, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Account(models.Model):
    # accountID = models.IntegerField(primary_key=True, choices=[(i, str(i)) for i in range(1000)])
    accountID = models.CharField(primary_key=True, max_length=10)
    level3ID = models.ForeignKey(AccountLevel3, on_delete=models.CASCADE, null=True, default=None)
    level2ID = models.ForeignKey(AccountLevel2, on_delete=models.CASCADE, null=True, default=None)
    level1ID = models.ForeignKey(AccountLevel1, on_delete=models.CASCADE, null=True, default=None)
    account_code = models.CharField(max_length=3, null=True)
    name = models.CharField(max_length=255)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, default=None, related_name='created_accounts')
    company_branch = models.ForeignKey(CompanyBranch, on_delete=models.CASCADE, default=None,
                                       related_name='created_accounts')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_accounts')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='updated_accounts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + "--" + self.accountID
