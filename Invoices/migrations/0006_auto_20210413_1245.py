# Generated by Django 2.2 on 2021-04-13 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Branches', '0001_initial'),
        ('Invoices', '0005_auto_20210407_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='main_warehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoice_main_warehouse', to='Branches.Warehouse', verbose_name='المخزن الرئيسي'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='sub_warehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoice_sub_warehouse', to='Branches.Warehouse', verbose_name='المخزن الفرعي'),
        ),
    ]
