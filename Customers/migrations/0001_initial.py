

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CallReason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='سبب الإتصال')),
                ('deleted', models.BooleanField(default=False, verbose_name='حذف')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='الاسم')),
                ('deleted', models.BooleanField(default=False, verbose_name='حذف')),
            ],
            options={
                'permissions': (('add_customer_category', 'إضافة شريحة عملاء'), ('edit_customer_category', 'تعديل شريحة عملاء'), ('delete_customer_category', 'حذف شريحة عملاء'), ('access_customer_category_menu', 'الدخول علي قائمة شرائح العملاء')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='الاسم')),
                ('phone', models.CharField(blank=True, max_length=14, null=True, verbose_name='التليفون')),
                ('address', models.TextField(blank=True, null=True, verbose_name='العنوان')),
                ('art_work', models.CharField(max_length=128, verbose_name='الفني')),
                ('payments_status', models.CharField(max_length=50, verbose_name='حالة الدفعات')),
                ('Products_status', models.CharField(max_length=50, verbose_name='حالة المنتجات')),
                ('seller_feedback', models.TextField(blank=True, null=True, verbose_name='ملاحظات البائع')),
                ('accountant_notes', models.TextField(blank=True, null=True, verbose_name='ملاحظات المحاسب')),
                ('secret', models.BooleanField(default=False, verbose_name='سري')),
                ('facebook_account', models.CharField(blank=True, max_length=128, null=True, verbose_name='حساب الفيس بوك')),
                ('job', models.CharField(blank=True, max_length=128, null=True, verbose_name='الوظيفة')),
                ('initial_balance', models.FloatField(default=0, verbose_name='الرصيد الافتتاحي')),
                ('allow_negative_balance', models.BooleanField(default=False, verbose_name='السماح بالبيع آجل')),
                ('max_negative_balance', models.FloatField(default=0, verbose_name='الحد الإئتماني')),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='أضيف بتاريخ')),
                ('deleted', models.BooleanField(default=False, verbose_name='حذف')),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='اضيف بواسطة')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Customers.Category', verbose_name='الشريحة')),
            ],
            options={
                'ordering': ['id'],
                'permissions': (('add_customer', 'إضافة عميل/مورد'), ('edit_customer', 'تعديل عميل/مورد'), ('delete_customer', 'حذف عميل/مورد'), ('view_customer', 'عرض بيانات عميل/مورد'), ('view_customer_balance', 'عرض رصيد عميل/مورد'), ('view_customer_statement', 'كشف حساب عميل/مورد'), ('access_customer_menu', 'الدخول علي قائمة العملاء/الموردين')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='CustomerCall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='التاريخ')),
                ('call_type', models.IntegerField(choices=[(1, 'مكالمة صادرة'), (2, 'مكالمة واردة'), (3, 'Whatsapp'), (4, 'Messenger')], verbose_name='نوع المكالمة')),
                ('summary', models.TextField(verbose_name='ملخص المكالمة')),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='الموظف')),
                ('call_reason', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Customers.CallReason', verbose_name='سبب المكالمة')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Customers.Customer', verbose_name='العميل')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='الاسم')),
                ('deleted', models.BooleanField(default=False, verbose_name='حذف')),
            ],
        ),
        migrations.CreateModel(
            name='Pricing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='اسم السعر')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='التاريخ')),
                ('title', models.CharField(max_length=128, verbose_name='عنوان الملاحظات')),
                ('note', models.TextField(verbose_name='محتوي الملاحظة')),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='الموظف')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Customers.Customer', verbose_name='العميل')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('history_type', models.IntegerField(choices=[(1, 'إضافة عميل'), (2, 'إضافة مكالمة'), (3, 'إضافة عرض سعر'), (4, 'إضافة فاتورة مبيعات'), (5, 'إضافة فاتورة مرتجع مبيعات'), (6, 'إضافة فاتورة مشتريات'), (7, 'إضافة فاتورة مرتجع مشتريات'), (8, 'إضافة ملاحظة'), (9, 'إضافة مكالمة'), (10, 'تحديد مهام')], verbose_name='نوع العملية')),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='التاريخ')),
                ('invoice_id', models.IntegerField(null=True, verbose_name='رقم الفاتورة')),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='الموظف')),
                ('call', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Customers.CustomerCall', verbose_name='المكالمة')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Customers.Customer', verbose_name='العميل')),
                ('note', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Customers.CustomerNote', verbose_name='الملاحظة')),
            ],
            options={
                'ordering': ['-added_at'],
            },
        ),
        migrations.AddField(
            model_name='customer',
            name='customer_type',
            field=models.ForeignKey(blank='True', null=True, on_delete=django.db.models.deletion.SET_NULL, to='Customers.CustomerType', verbose_name='نوع العميل'),
        ),
        migrations.AddField(
            model_name='customer',
            name='main_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Customers.Customer', verbose_name='الحساب الرئيسي'),
        ),
    ]
