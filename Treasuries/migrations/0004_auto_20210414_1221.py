# Generated by Django 2.2 on 2021-04-14 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Treasuries', '0003_paymentmachines'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmachines',
            name='transfer',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='لتحويل الى'),
        ),
    ]
