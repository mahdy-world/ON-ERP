# Generated by Django 2.2 on 2021-04-04 12:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Customers', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PrintSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.IntegerField(choices=[(1, 'A4/A5'), (2, 'طابعة ريسيت 8سم')], default=1, verbose_name='حجم الطباعة')),
                ('name', models.CharField(blank=True, max_length=128, null=True, verbose_name='اسم الشركة')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='', verbose_name='اللوجو')),
                ('logo_width', models.FloatField(default=100, verbose_name='نسبة عرض اللوجو في الإيصال')),
                ('logo_location', models.IntegerField(choices=[(1, 'يمين الفاتورة'), (2, 'يسار الفاتورة')], default=1, verbose_name='موقع اللوجو')),
                ('text_size', models.FloatField(default=12, verbose_name='حجم الخط في الوصل')),
                ('sales_invoice_title', models.CharField(default='إيصال صيانة', max_length=128, verbose_name='عنوان الإيصال')),
                ('footer1', models.TextField(blank=True, null=True, verbose_name='النص 1')),
                ('footer2', models.TextField(blank=True, null=True, verbose_name='النص 2')),
                ('footer1_location', models.IntegerField(choices=[(1, 'أعلي الإيصال'), (2, 'أسفل الإيصال')], default=2, verbose_name='موضع النص 1')),
            ],
            options={
                'permissions': (('edit_maintenance_receipt_setting', 'تعديل إعدادات طباعة إيصالات الصيانة'),),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاريخ فتح التذكرة')),
                ('sn', models.CharField(blank=True, max_length=128, null=True, verbose_name='السيريال')),
                ('maintenance_type', models.PositiveSmallIntegerField(choices=[(1, 'صيانة'), (2, 'ضمان')], default=1, verbose_name='نوع الصيانة')),
                ('problem', models.TextField(verbose_name='المشكلة')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='ملاحظات')),
                ('diagnosis', models.TextField(verbose_name='التشخيص')),
                ('cost', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='التكلفة')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'قيد التشخيص'), (2, 'قيد التقييم'), (3, 'في انتظار رد العميل'), (4, 'العميل يرفض التكلفة'), (5, 'العميل يرفض فترة الإصلاح'), (6, 'قيد الإصلاح'), (7, 'تمت الصيانة'), (8, 'لا يمكن الإصلاح')], default=1, verbose_name='حالة التذكرة')),
                ('outsource_status', models.PositiveSmallIntegerField(choices=[(1, 'صيانة داخلية'), (2, 'تم تحويلها لصيانة خارجية'), (3, 'تم استلامها من الصيانة الخارجية')], default=1)),
                ('outsource', models.CharField(blank=True, max_length=128, null=True, verbose_name='حولت إلي')),
                ('shipping_company', models.CharField(blank=True, max_length=128, null=True, verbose_name='شركة الشحن')),
                ('shipping_id', models.CharField(blank=True, max_length=128, null=True, verbose_name='بوليصة الشحن')),
                ('shipping_company2', models.CharField(blank=True, max_length=128, null=True, verbose_name='شركة الشحن')),
                ('shipping_id2', models.CharField(blank=True, max_length=128, null=True, verbose_name='بوليصة الشحن')),
                ('customer_received', models.BooleanField(default=False, verbose_name='استلام')),
                ('customer_reply', models.PositiveSmallIntegerField(choices=[(1, 'لم يتم الرد'), (2, 'العميل موافق علي التكلفة'), (3, 'العميل يرفض التكلفة')], default=0, verbose_name='رد العميل')),
                ('reject_reason', models.TextField(blank=True, null=True, verbose_name='سبب رفض الصيانة')),
                ('done', models.BooleanField(default=False, verbose_name='تمت الصيانة؟')),
                ('deleted', models.BooleanField(default=False, verbose_name='حذف')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Customers.Customer', verbose_name='العميل')),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='موجه إلي')),
            ],
            options={
                'ordering': ['-id'],
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='TicketReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='التوقيت')),
                ('reply', models.TextField(verbose_name='الرد')),
                ('notify_customer', models.BooleanField(default=False, verbose_name='تنبيه العميل؟')),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='الموظف')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Maintenance.Ticket', verbose_name='رقم التذكرة')),
            ],
            options={
                'ordering': ['-id'],
                'default_permissions': (),
            },
        ),
    ]
