# Generated by Django 4.2 on 2023-12-16 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_companybranch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='companybranch',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
