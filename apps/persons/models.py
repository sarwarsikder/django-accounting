from django.db import models

from apps.company.models import Company, CompanyBranch


# Create your models here.

class Person(models.Model):
    CUSTOMER = 'customer'
    SUPPLIER = 'supplier'

    PERSON_TYPE_CHOICES = [
        (CUSTOMER, 'Customer'),
        (SUPPLIER, 'Supplier'),
    ]

    personsID = models.AutoField(primary_key=True)
    persons_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255, null=True, blank=True, default="")
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, default=None, related_name='persons')
    company_branch = models.ForeignKey(CompanyBranch, on_delete=models.CASCADE, default=None, related_name='persons')
    mobile = models.CharField(max_length=20)
    mobile2 = models.CharField(max_length=20, null=True, blank=True)
    occupation = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    active = models.CharField(max_length=5, choices=[('yes', 'Yes'), ('no', 'No'), ('leave', 'Leave')])
    person_type = models.CharField(max_length=10, choices=PERSON_TYPE_CHOICES)

    def __str__(self):
        return self.persons_name
