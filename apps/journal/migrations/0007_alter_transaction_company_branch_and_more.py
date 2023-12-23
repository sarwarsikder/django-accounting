# Generated by Django 4.2 on 2023-12-23 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_alter_company_id_alter_companybranch_id'),
        ('journal', '0006_alter_document_company_branch_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='company_branch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='company.companybranch'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='company_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='company.company'),
        ),
    ]
