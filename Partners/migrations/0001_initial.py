# Generated by Django 2.2 on 2021-04-04 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='اسم الشريك')),
                ('phone', models.CharField(max_length=11, verbose_name='رقم الهاتف')),
                ('initial_balance', models.FloatField(default=0, verbose_name='الرصيد الافتتاحي')),
                ('deleted', models.BooleanField(default=False, verbose_name='حذف')),
            ],
            options={
                'permissions': (('add_partner', 'إضافة شريك'), ('edit_partner', 'تعديل شريك'), ('delete_partner', 'حذف شريك'), ('view_partner', 'عرض بيانات شريك'), ('view_partner_balance', 'عرض رصيد شريك'), ('view_partner_statement', 'كشف حساب شريك'), ('access_partner_menu', 'الدخول علي قائمة الشركاء')),
                'default_permissions': (),
            },
        ),
    ]
