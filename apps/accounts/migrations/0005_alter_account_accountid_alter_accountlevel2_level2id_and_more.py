# Generated by Django 4.2 on 2023-12-27 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_accountlevel1_level1id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='accountID',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='accountlevel2',
            name='level2ID',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='accountlevel3',
            name='level3ID',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
