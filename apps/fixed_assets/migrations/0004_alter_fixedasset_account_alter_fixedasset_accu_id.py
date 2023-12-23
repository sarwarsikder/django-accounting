# Generated by Django 4.2 on 2023-12-23 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_account_level1id_account_level2id_and_more'),
        ('fixed_assets', '0003_alter_fixedasset_depreciation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixedasset',
            name='account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.account'),
        ),
        migrations.AlterField(
            model_name='fixedasset',
            name='accu_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fixed_assets.depreciationcategory'),
        ),
    ]
