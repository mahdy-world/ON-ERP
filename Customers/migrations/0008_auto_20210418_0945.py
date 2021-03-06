# Generated by Django 2.2 on 2021-04-18 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0007_auto_20210418_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='job',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='مجموعه فرعيه'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='technician',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Technicians.Technician', verbose_name='الفني الافتراضي'),
        ),
    ]
