# Generated by Django 4.2 on 2023-12-23 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0007_alter_transaction_company_branch_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
