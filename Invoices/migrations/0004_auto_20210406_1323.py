# Generated by Django 2.2 on 2021-04-06 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Invoices', '0003_auto_20210406_1234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='cost_profit',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='purchase_profit',
        ),
        migrations.RemoveField(
            model_name='invoiceitem',
            name='cost_profit',
        ),
        migrations.RemoveField(
            model_name='invoiceitem',
            name='purchase_profit',
        ),
        migrations.AddField(
            model_name='invoice',
            name='invoice_discount',
            field=models.FloatField(default=0.0, verbose_name='خصم خاص علي الفاتورة'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='profit',
            field=models.FloatField(default=0.0, verbose_name='الربح'),
        ),
        migrations.AddField(
            model_name='invoiceitem',
            name='profit',
            field=models.FloatField(default=0.0, verbose_name='الربح'),
        ),
    ]
