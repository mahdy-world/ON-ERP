# Generated by Django 2.2 on 2021-04-04 12:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='التاريخ')),
                ('invoice_type', models.IntegerField(choices=[(1, 'فاتورة مبيعات'), (2, 'فاتورة مبيعات توصيل'), (3, 'فاتورة مبيعات موقع'), (4, 'فاتورة مرتجع مبيعات'), (5, 'فاتورة مشتريات'), (6, 'فاتورة مرتجع مشتريات'), (7, 'عرض أسعار'), (8, 'مصروفات عامة'), (9, 'دخل عام'), (10, 'حساب جاري الشركاء'), (11, 'إذن صرف نقدية'), (12, 'إذن قبض نقدية'), (13, 'إضافة رأس مال'), (14, 'سحب من رأس المال'), (15, 'فاتورة تسوية عجز'), (16, 'فاتورة تسوية زيادة'), (17, 'تحويل مخزون'), (19, 'تحويل خزينة'), (21, 'قبض سداد'), (22, 'صرف سداد')], verbose_name='نوع الفاتورة')),
                ('treasury_in', models.FloatField(default=0.0, verbose_name='دخل الخزينة / وارد')),
                ('treasury_out', models.FloatField(default=0.0, verbose_name='مصروف من الخزينة / منصرف')),
                ('customer_debit', models.FloatField(default=0.0, verbose_name='العميل له')),
                ('customer_credit', models.FloatField(default=0.0, verbose_name='العميل عليه')),
                ('total', models.FloatField(default=0.0, verbose_name='إجمالي الفاتورة')),
                ('discount', models.FloatField(default=0.0, verbose_name='الخصم')),
                ('after_discount', models.FloatField(default=0.0, verbose_name='بعد الخصم')),
                ('shipping', models.FloatField(default=0.0, verbose_name='تكلفة الشحن')),
                ('overall', models.FloatField(default=0.0, verbose_name='إجمالي')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='ملاحظات')),
                ('internal_comment', models.TextField(blank=True, null=True, verbose_name='ملاحظات داخلية')),
                ('saved', models.BooleanField(default=False, verbose_name='حفظ')),
                ('paid', models.BooleanField(default=False, verbose_name='دفع')),
                ('numbering', models.IntegerField(default=0, verbose_name='ترقيم')),
                ('out_of_warehouse', models.BooleanField(default=False, verbose_name='خروج من المخزن')),
                ('deleted', models.BooleanField(default=False, verbose_name='حذف')),
                ('cost_profit', models.FloatField(default=0.0, verbose_name='ربح التكلفة')),
                ('purchase_profit', models.FloatField(default=0.0, verbose_name='ربح الشراء')),
            ],
            options={
                'ordering': ['date'],
                'permissions': (('undo_save_invoice', 'إعادة فتح الفواتير'), ('add_sales_invoice', 'إضافة فاتورة مبيعات'), ('delete_invoice', 'حذف الفواتير'), ('permanent_delete_invoices', 'حذف نهائي للفواتير'), ('restore_deleted_invoices', 'إستعادة الفواتير المحذوفة'), ('access_sales_invoice_menu', 'عرض فواتير المبيعات'), ('add_reverse_sales_invoice', 'إضافة فاتورة مرتجع مبيعات'), ('access_reverse_sales_invoice_menu', 'عرض فواتير مرتجع المبيعات'), ('add_purchase_invoice', 'إضافة فاتورة مشتريات'), ('access_purchase_invoice_menu', 'عرض فواتير المشتريات'), ('add_reverse_purchase_invoice', 'إضافة فاتورة مرتجع مشتريات'), ('access_reverse_purchase_invoice_menu', 'عرض فواتير مرتجع المشتريات'), ('access_quotation', 'مشاهدة عروض الاسعار'), ('add_quotation', 'إضافة عروض أسعار'), ('add_branch_transfer', 'إضافة تحويل مخزن'), ('delete_branch_transfer', 'حذف تحويل مخزن'), ('access_branch_transfer_menu', 'عرض  تحويل مخزن'), ('add_treasury_transfer', 'إضافة تحويل نقدية'), ('delete_treasury_transfer', 'حذف تحويل نقدية'), ('access_treasury_transfer_menu', 'عرض  تحويل نقدية'), ('add_income_invoice', 'إضافة سند قبض نقدية'), ('delete_income_invoice', 'حذف سند قبض نقدية'), ('access_income_invoice_menu', 'عرض سندات قبض نقدية'), ('add_outcome_invoice', 'إضافة سند صرف نقدية'), ('delete_outcome_invoice', 'حذف سند صرف نقدية'), ('access_outcome_invoice_menu', 'عرض سندات صرف نقدية'), ('add_capital', 'إضافة لرأس المال'), ('minus_capital', 'سحب من رأس المال'), ('add_stock_plus_invoice', 'إضافة فاتورة تسوية زيادة'), ('access_stock_plus_invoice', 'عرض فاتورة تسوية زيادة'), ('add_stock_minus_invoice', 'إضافة فاتورة تسوية عجز'), ('access_stock_minus_invoice', 'عرض فاتورة تسوية عجز'), ('access_sales_invoice_report', 'عرض تقارير فواتير المبيعات'), ('access_reverse_sales_invoice_report', 'عرض تقارير فواتير المبيعات'), ('access_purchase_invoice_report', 'عرض تقارير فواتير المبيعات'), ('access_reverse_purchase_invoice_report', 'عرض تقارير فواتير المبيعات'), ('access_quotation_report', 'عرض تقارير عروض الاسعار'), ('show_profit', 'عرض الارباح'), ('edit_invoice_date', 'تعديل التاريخ في الفاتورة'), ('invoice_discount', 'عمل خصم علي الفاتورة'), ('item_discount', 'عمل خصم علي المنتجات'), ('edit_item_unit_price', 'تعديل سعر المنتج في الفاتورة'), ('edit_invoice_setting', 'تعديل إعدادات الفواتير'), ('edit_invoice_print_setting', 'تعديل إعدادات طباعة الفواتير'), ('add_customer_income', 'قبض سداد عميل/مورد'), ('add_customer_outcome', 'صرف سداد عميل/مورد')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='InvoiceBaseSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sell_without_stock', models.BooleanField(default=False, verbose_name='السماح بالبيع في حالة عدم وجود مخزون كافي')),
                ('alert_on_critical_storage', models.BooleanField(default=True, verbose_name='تحذير عند الوصول للرصيد الحرج')),
                ('view_profit_in_invoice', models.BooleanField(default=True, verbose_name='عرض الربح أثناء عمل الفاتورة (لا يظهر الا لمن يمتلك هذه الخاصية)')),
                ('update_cost_profit_on_purchase', models.BooleanField(default=True, verbose_name='تحديث سعر التكلفة تلقائي عند الشراء')),
                ('alert_on_min_cost_price', models.BooleanField(default=True, verbose_name='تحذير عند البيع بأقل من سعر التكلفة')),
                ('alert_on_min_purchase_price', models.BooleanField(default=True, verbose_name='تحذير عند البيع بأقل من سعر الشراء')),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=1.0, verbose_name='الكمية')),
                ('unit_price', models.FloatField(default=0.0, verbose_name='سعر الوحدة')),
                ('total_price', models.FloatField(default=0.0, verbose_name='إجمالي')),
                ('discount', models.FloatField(default=0.0, verbose_name='خصم')),
                ('after_discount', models.FloatField(default=0.0, verbose_name='بعد الخصم')),
                ('comment', models.CharField(blank=True, max_length=64, null=True, verbose_name='ملاحظات')),
                ('main_warehouse', models.FloatField(default=0.0, verbose_name='من/الي المخزن الرئيسي')),
                ('sub_warehouse', models.FloatField(default=0.0, verbose_name='من/الي المخزن الفرعي')),
                ('deleted', models.BooleanField(default=False, verbose_name='حذف المنتج من الفاتورة')),
                ('main_unit_quantity', models.FloatField(default=0.0, verbose_name='الكمية بالوحدة الأساسية')),
                ('main_unit_main_warehouse', models.FloatField(default=0.0, verbose_name='الكمية بالوحدة الأساسية في المخزن الرئيسي')),
                ('main_unit_sub_warehouse', models.FloatField(default=0.0, verbose_name='الكمية بالوحدة الأساسية في المخزن الفرعي')),
                ('cost_profit', models.FloatField(default=0.0, verbose_name='ربح التكلفة')),
                ('purchase_profit', models.FloatField(default=0.0, verbose_name='ربح الشراء')),
            ],
            options={
                'permissions': (('delete_item_from_invoice', 'حذف منتج من الفاتورة'),),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='InvoiceSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.IntegerField(choices=[(1, 'A4/A5'), (2, 'طابعة ريسيت 8سم')], default=1, verbose_name='حجم الطباعة')),
                ('name', models.CharField(blank=True, max_length=128, null=True, verbose_name='اسم الشركة')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='', verbose_name='اللوجو')),
                ('logo_width', models.FloatField(default=100, verbose_name='نسبة عرض اللوجو في الفاتورة')),
                ('logo_location', models.IntegerField(choices=[(1, 'يمين الفاتورة'), (2, 'يسار الفاتورة')], default=1, verbose_name='موقع اللوجو')),
                ('text_size', models.FloatField(default=12, verbose_name='حجم الخط في الفاتورة')),
                ('sales_invoice_title', models.CharField(default='فاتورة مبيعات', max_length=128, verbose_name='عنوان فاتورة المبيعات')),
                ('print_items_discount', models.BooleanField(default=False, verbose_name='طباعة الخصم بجوار المنتجات')),
                ('print_product_description', models.BooleanField(default=False, verbose_name='طباعة وصف المنتج')),
                ('print_product_comments', models.BooleanField(default=False, verbose_name='طباعة ملاحظات المنتج في الفاتورة')),
                ('print_invoice_comments', models.BooleanField(default=False, verbose_name='طباعة ملاحظات الفاتورة')),
                ('print_account_summary', models.BooleanField(default=False, verbose_name='طباعة ملخص حسابات العميل في الفاتورة')),
                ('footer1', models.TextField(blank=True, null=True, verbose_name='النص 1')),
                ('footer2', models.TextField(blank=True, null=True, verbose_name='النص 2')),
                ('footer1_location', models.IntegerField(choices=[(1, 'أعلي الفاتورة'), (2, 'أسفل الفاتورة')], default=2, verbose_name='موضع النص 1')),
            ],
            options={
                'permissions': (('edit_invoice_setting', 'تعديل إعدادات طباعة الفواتير'),),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='SpendCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='اسم التصنيف')),
                ('deleted', models.BooleanField(default=False, verbose_name='حذف')),
            ],
            options={
                'permissions': (('add_spend_category', 'إضافة تصنيف مصروفات'), ('edit_spend_category', 'تعديل تصنيف مصروفات'), ('delete_spend_category', 'حذف تصنيف مصروفات'), ('access_spend_category_menu', 'الدخول علي قائمة تصنيفات المصروفات')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='TreasuryTransactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction', models.CharField(blank=True, max_length=64, null=True, verbose_name='عملية')),
                ('incoming', models.FloatField(default=0.0, verbose_name='وارد')),
                ('outgoing', models.FloatField(default=0.0, verbose_name='منصرف')),
                ('balance', models.FloatField(default=0.0, verbose_name='رصيد')),
                ('total_incoming', models.FloatField(default=0.0, verbose_name='إجمالي وارد')),
                ('total_outgoing', models.FloatField(default=0.0, verbose_name='إجمالي منصرف')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='ملاحظات')),
                ('deleted', models.BooleanField(default=False, verbose_name='حذف')),
            ],
        ),
        migrations.CreateModel(
            name='WarehouseTransactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incoming', models.FloatField(default=0.0, verbose_name='وارد')),
                ('outgoing', models.FloatField(default=0.0, verbose_name='منصرف')),
                ('balance', models.FloatField(default=0.0, verbose_name='رصيد')),
                ('total_incoming', models.FloatField(default=0.0, verbose_name='إجمالي وارد')),
                ('total_outgoing', models.FloatField(default=0.0, verbose_name='إجمالي منصرف')),
                ('deleted', models.BooleanField(default=False, verbose_name='حذف')),
            ],
        ),
    ]
