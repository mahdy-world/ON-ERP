# Generated by Django 2.2 on 2021-04-14 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Treasuries', '0005_auto_20210414_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmachines',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]