# Generated by Django 2.2 on 2021-04-04 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BarcodeSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('width', models.FloatField(default=5, verbose_name='عرض الملصق بالسنتيمتر')),
                ('height', models.FloatField(default=1, verbose_name='طول الملصق بالسنتيمتر')),
                ('font_size', models.FloatField(default=8, verbose_name='حجم الخط')),
                ('company_name', models.CharField(default='الشركة', max_length=32, verbose_name='اسم الشركة')),
                ('print_company_name', models.BooleanField(default=True, verbose_name='طباعة اسم الشركة')),
                ('print_price', models.BooleanField(default=True, verbose_name='طباعة السعر')),
                ('print_product_name', models.BooleanField(default=True, verbose_name='طباعة اسم المنتج')),
            ],
            options={
                'permissions': (('edit_barcode_setting', 'تعديل إعدادات الباركود'),),
                'default_permissions': (),
            },
        ),
    ]
