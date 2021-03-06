# Generated by Django 2.2 on 2021-04-14 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Branches', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMachines',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='الاسم')),
                ('discount_percentage', models.FloatField(default=0, verbose_name='نسبة الخسم')),
                ('transfer', models.IntegerField(blank=True, null=True, verbose_name='التحويل الى')),
            ],
        ),
    ]
