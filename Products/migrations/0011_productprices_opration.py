# Generated by Django 2.2 on 2021-04-15 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0010_auto_20210415_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='productprices',
            name='opration',
            field=models.IntegerField(choices=[(1, '-'), (2, '+')], default=1, verbose_name='العملية'),
        ),
    ]