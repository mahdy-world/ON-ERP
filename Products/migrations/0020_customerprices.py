# Generated by Django 2.2 on 2021-04-19 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0011_auto_20210418_1151'),
        ('Products', '0019_auto_20210418_1514'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerPrices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False, verbose_name='مسح')),
                ('customer_segment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Customers.Category', verbose_name='الشريحة')),
                ('prices_list', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Products.PricesList', verbose_name='اسم قائمة الاسعار')),
            ],
        ),
    ]
