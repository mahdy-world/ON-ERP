# Generated by Django 2.2 on 2021-04-06 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Invoices', '0002_auto_20210404_1419'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='warehousetransactions',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='warehousetransactions',
            name='total_outgoing',
        ),
        migrations.AddField(
            model_name='warehousetransactions',
            name='purchase_cost',
            field=models.FloatField(default=0.0, verbose_name='سعر الشراء'),
        ),
        migrations.AlterField(
            model_name='warehousetransactions',
            name='incoming',
            field=models.FloatField(default=0.0, verbose_name='كمية الوارد'),
        ),
        migrations.AlterField(
            model_name='warehousetransactions',
            name='outgoing',
            field=models.FloatField(default=0.0, verbose_name='كمية المنصرف'),
        ),
        migrations.AlterField(
            model_name='warehousetransactions',
            name='total_incoming',
            field=models.FloatField(default=0.0, verbose_name='قيمة إجمالي الوارد'),
        ),
    ]
