# Generated by Django 2.2 on 2021-04-19 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0022_customerprices_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerprices',
            name='price',
        ),
    ]