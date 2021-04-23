# Generated by Django 2.2 on 2021-04-15 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0011_productprices_opration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='accountant_comment',
        ),
        migrations.RemoveField(
            model_name='product',
            name='sales_man_comment',
        ),
        migrations.AddField(
            model_name='product',
            name='product_card_comment',
            field=models.TextField(blank=True, null=True, verbose_name='ملاحظات كارت صنف'),
        ),
        migrations.AddField(
            model_name='product',
            name='supplier_comment',
            field=models.TextField(blank=True, null=True, verbose_name='ملاحظات مورد'),
        ),
    ]
