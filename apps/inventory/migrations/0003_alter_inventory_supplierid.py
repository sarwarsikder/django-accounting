# Generated by Django 4.2 on 2023-12-19 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0006_alter_person_user_name'),
        ('inventory', '0002_rename_accountid_inventory_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='supplierID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='persons.person'),
        ),
    ]
