# Generated by Django 2.2 on 2021-04-04 12:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Products', '0001_initial'),
        ('Customers', '__first__'),
        ('Branches', '0001_initial'),
        ('Invoices', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Treasuries', '0001_initial'),
        ('Partners', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='warehousetransactions',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Products.Product', verbose_name='المنتج'),
        ),
        migrations.AddField(
            model_name='warehousetransactions',
            name='warehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Branches.Warehouse', verbose_name='المخزن'),
        ),
        migrations.AddField(
            model_name='treasurytransactions',
            name='treasury',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Treasuries.Treasury', verbose_name='الخزينة'),
        ),
        migrations.AddField(
            model_name='invoiceitem',
            name='invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Invoices.Invoice', verbose_name='الفاتورة'),
        ),
        migrations.AddField(
            model_name='invoiceitem',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Products.Product', verbose_name='المنتج'),
        ),
        migrations.AddField(
            model_name='invoiceitem',
            name='unit_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Products.Unit', verbose_name='الوحدة'),
        ),
        migrations.AddField(
            model_name='invoicebasesetting',
            name='default_customer_in_sales',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Customers.Customer', verbose_name='العميل الافتراضي لفاتورة المبيعات'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='منشئ الفاتورة'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Customers.Customer', verbose_name='العميل / المورد'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='from_branch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='branch_out_transactions', to='Branches.Branch', verbose_name='من فرع'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='from_treasury',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='treasury_out_transactions', to='Treasuries.Treasury', verbose_name='من خزينة'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='from_warehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='warehouse_out_transactions', to='Branches.Warehouse', verbose_name='من مخزن'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='partner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Partners.Partner', verbose_name='الشريك'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='spend_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Invoices.SpendCategory', verbose_name='التصنيف'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='to_branch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='branch_in_transactions', to='Branches.Branch', verbose_name='إلي فرع'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='to_treasury',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='treasury_in_transactions', to='Treasuries.Treasury', verbose_name='إلي خزينة'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='to_warehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='warehouse_in_transactions', to='Branches.Warehouse', verbose_name='الي مخزن'),
        ),
    ]
