# Generated by Django 2.2 on 2021-04-15 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0009_auto_20210413_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='productprices',
            name='discount',
            field=models.FloatField(default=0.0, verbose_name='نسبة الخصم '),
        ),
        migrations.AddField(
            model_name='productprices',
            name='new_price',
            field=models.FloatField(default=0.0, verbose_name='السعر بعد الخصم'),
        ),
    ]
