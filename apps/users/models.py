from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from apps.company.models import Company, CompanyBranch

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    pass


class CustomUser(AbstractUser):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True, related_name='users')
    company_branch = models.ForeignKey(CompanyBranch, on_delete=models.CASCADE, blank=True, null=True,
                                       related_name='users')
    mobile = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
