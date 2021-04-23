# Generated by Django 2.2 on 2021-04-14 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Treasuries', '0004_auto_20210414_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmachines',
            name='transfer',
            field=models.ForeignKey(blank=True, max_length=128, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Treasuries.Treasury', verbose_name='لتحويل الى'),
        ),
        migrations.AlterField(
            model_name='treasury',
            name='type',
            field=models.IntegerField(choices=[(1, 'خزينة'), (2, 'حساب بنكي'), (3, 'حساب عهدة'), (4, 'حساب سلف رواتب'), (5, 'حاقظة اوراق دفع'), (6, 'حاقظة اوراق قبض')], verbose_name='النوع'),
        ),
    ]