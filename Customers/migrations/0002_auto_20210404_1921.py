# Generated by Django 2.2 on 2021-04-04 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Technicians', '0002_technician_phone'),
        ('Customers', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='art_work',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='category',
        ),
        migrations.AddField(
            model_name='customer',
            name='purchases_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vendors_category', to='Customers.Category', verbose_name='شريحة المشتريات'),
        ),
        migrations.AddField(
            model_name='customer',
            name='sales_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customers_category', to='Customers.Category', verbose_name='شريحة المبيعات'),
        ),
        migrations.AddField(
            model_name='customer',
            name='technician',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Technicians.Technician'),
        ),
    ]