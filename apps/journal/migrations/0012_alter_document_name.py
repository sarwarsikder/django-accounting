# Generated by Django 4.2 on 2023-12-27 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0011_alter_transaction_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='name',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
