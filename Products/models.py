from django.db import models
from django.db.models import Sum
from datetime import date

from Branches.models import Warehouse, Branch
from Customers.models import Category, Customer
from django.conf import settings


# Create your models here.
class MainCategory(models.Model):
    name = models.CharField(max_length=128, verbose_name='الاسم')
    deleted = models.BooleanField(default=False, verbose_name='مسح')

    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_main_category', 'إضافة تصنيف رئيسي للمنتجات'),
            ('edit_main_category', 'تعديل تصنيف رئيسي للمنتجات'),
            ('delete_main_category', 'حذف تصنيف رئيسي للمنتجات'),
            ('access_main_category_menu', 'الدخول علي التصنيف الرئيسية للمنتجات'),
        )


class SubCategory(models.Model):
    name = models.CharField(max_length=128, verbose_name='الاسم')
    main_category = models.ForeignKey(MainCategory, on_delete=models.SET_NULL, null=True, blank=True,
                                      verbose_name='المجموعة الرئيسية')
    deleted = models.BooleanField(default=False, verbose_name='مسح')

    def __str__(self):
        if self.main_category:
            return self.main_category.name + ' - ' + self.name
        else:
            return self.name

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_sub_category', 'إضافة تصنيف فرعي للمنتجات'),
            ('edit_sub_category', 'تعديل تصنيف فرعي للمنتجات'),
            ('delete_sub_category', 'حذف تصنيف فرعي للمنتجات'),
            ('access_sub_category_menu', 'الدخول علي التصنيف الفرعية للمنتجات'),
        )


class Manufacture(models.Model):
    name = models.CharField(max_length=128, verbose_name='الاسم')
    deleted = models.BooleanField(default=False, verbose_name='مسح')

    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_manufacture', 'إضافة جهة مصنعة للمنتجات'),
            ('edit_manufacture', 'تعديل جهة مصنعة للمنتجات'),
            ('delete_manufacture', 'حذف جهة مصنعة للمنتجات'),
            ('access_manufacture_menu', 'الدخول علي قائمة الجهات المصنعة'),
        )


class Brand(models.Model):
    name = models.CharField(max_length=128, verbose_name='الاسم')
    deleted = models.BooleanField(default=False, verbose_name='مسح')

    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_brand', 'إضافة براند'),
            ('edit_brand', 'تعديل براند'),
            ('delete_brand', 'حذف براند'),
            ('access_brand_menu', 'الدخول علي قائمة البراندات'),
        )


class Unit(models.Model):
    name = models.CharField(max_length=128, verbose_name='الاسم')
    deleted = models.BooleanField(default=False, verbose_name='مسح')

    def __str__(self):
        return self.name


class PricesList(models.Model):
    op = (
        (1, '-'),
        (2, '+'),
    )
    name = models.CharField(max_length=128, verbose_name='الاسم')
    deleted = models.BooleanField(default=False, verbose_name='مسح')

    def __str__(self):
        return self.name


class Product(models.Model):
    types = (
        (1, 'منتج عادي'),
        (2, 'منتج مجمع'),
        (3, 'خدمة'),
    )
    color = (
        ('#FFFFFF', ''),
        ('#FF0000', 'احمر'),
        ('#fff400', 'اصفر'),
        ('#00c33e', 'اخضر'),
    )
    product_type = models.IntegerField(choices=types, default=1, verbose_name='النوع')
    name = models.CharField(max_length=128, verbose_name='الاسم')
    description = models.TextField(verbose_name='وصف المنتج', null=True, blank=True)
    sub_category = models.ManyToManyField(SubCategory, null=True, blank=True,
                                     verbose_name='مجموعه البدائل ')
    manufacture = models.ForeignKey(Manufacture, on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name='الجهة المصنعة')
    brand = models.ManyToManyField(Brand, null=True, blank=True, verbose_name='الكتالوج')
    deleted = models.BooleanField(default=False, verbose_name='مسح')
    sell_price = models.FloatField(default=0.0, verbose_name='سعر البيع الرئيسي')
    cost_price = models.FloatField(default=0.0, verbose_name='سعر التكلفة الرئيسي')
    purchase_price = models.FloatField(default=0.0, verbose_name='سعر الشراء الرئيسي')
    main_unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, 
                                  verbose_name='الوحدة الاساسية', related_name='main_unit')
    initial_value = models.FloatField(default=0.0, verbose_name='القيمة الافتتاحية')
    initial_branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True,verbose_name='الفرع الافتتاحي')
    max_sell = models.FloatField(verbose_name='حد الصرف', null=True, blank=True)
    full_stock = models.FloatField(verbose_name='حد الطلب', null=True, blank=True)
    critical_stock_for_one_warehouse = models.FloatField(verbose_name='الرصيد الحرج للمخزن الواحد', default=1)
    critical_stock_for_one_branch = models.FloatField(verbose_name='الرصيد الحرج للفرع الواحد', default=1)
    critical_stock_for_all_branches = models.FloatField(verbose_name='الرصيد الحرج لجميع الفروع', default=1)
    forbid_for_reverse = models.BooleanField(default=False, verbose_name='ممنوع من المرتجع')
    forbid_customer_group = models.ManyToManyField(Customer, verbose_name='إيقاف البيع لشرائح معينة', null=True, blank=True)
    product_card_comment = models.TextField(verbose_name='ملاحظات كارت صنف', null=True, blank=True)
    supplier_comment = models.TextField(verbose_name='ملاحظات مورد', null=True, blank=True)
    print_comment = models.TextField(verbose_name='ملاحظات للورقة المطبوعة', null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    sell_price_last_update = models.DateTimeField(auto_now=True, verbose_name='آخر تحديث للسعر')
    price_list = models.ForeignKey(PricesList, on_delete=models.CASCADE, null=True, blank=True, verbose_name='اسم قائمة الأسعار')
    purchase_price_new= models.FloatField(default=0.0, verbose_name='سعر شراء للجديد')
    purchase_price_new_activation = models.BooleanField(default=False, verbose_name='تنشيط سعر الشراء الجديد')
    purchase_price_new_comment = models.TextField(verbose_name='ملاحظات سعر شراء جديد', null=True, blank=True)
    bonus = models.CharField(default="#FFFFFF", choices=color , max_length=50, verbose_name='درجه البونص')
    
    

    def __str__(self):
        return self.name

    def current_stock(self):
        stock_in_invoices = [4, 5, 16]
        stock_out_invoices = [1, 2, 3, 6, 15]
        stock_in = self.magedinvoiceitems_set.all().filter(invoice__deleted=False, invoice__out_of_warehouse=True,
                                                     item__product_type__in=[1, 2],
                                                     invoice__invoice_type__in=stock_in_invoices).aggregate(
            total=Sum('main_unit_quantity'))
        if stock_in['total'] is None:
            stock_in['total'] = 0
        stock_out = self.magedinvoiceitems_set.all().filter(invoice__deleted=False, invoice__out_of_warehouse=True,
                                                      item__product_type__in=[1, 2],
                                                      invoice__invoice_type__in=stock_out_invoices).aggregate(
            total=Sum('main_unit_quantity'))
        if stock_out['total'] is None:
            stock_out['total'] = 0
        total = stock_in['total'] - stock_out['total']
        return total

    def current_stock_value(self):
        if not self.current_stock() is None:
            return self.cost_price * self.current_stock()
        else:
            return 0

    def branch_stock(self, branch):
        stock_in_invoices = [4, 5, 16, 17]
        stock_out_invoices = [1, 2, 3, 6, 15, 17]
        stock_in = self.magedinvoiceitems_set.all().filter(invoice__branch_id=branch, invoice__deleted=False,
                                                     invoice__saved=True, item__product_type__in=[1, 2],
                                                     invoice__invoice_type__in=stock_in_invoices).aggregate(
            total=Sum('main_unit_quantity'))
        if stock_in['total'] is None:
            stock_in['total'] = 0

        stock_out = self.magedinvoiceitems_set.all().filter(invoice__branch_id=branch, invoice__deleted=False,
                                                        invoice__saved=True, item__product_type__in=[1, 2],
                                                      invoice__invoice_type__in=stock_out_invoices).aggregate(
            total=Sum('main_unit_quantity'))
        if stock_out['total'] is None:
            stock_out['total'] = 0
        total = stock_in['total'] - stock_out['total']
        return total


    def main_store_stock(self, store):
        stock_in_invoices = [4, 5, 16, 17]
        stock_out_invoices = [1, 2, 3, 6, 15, 17]
        stock_in = self.magedinvoiceitems_set.all().filter(invoice__main_warehouse_id=store, invoice__deleted=False,
                                                           invoice__saved=True, item__product_type__in=[1, 2],
                                                           invoice__invoice_type__in=stock_in_invoices).aggregate(
            total=Sum('main_unit_main_warehouse'))
        if stock_in['total'] is None:
            stock_in['total'] = 0

        stock_out = self.magedinvoiceitems_set.all().filter(invoice__main_warehouse_id=store, invoice__deleted=False,
                                                            invoice__saved=True, item__product_type__in=[1, 2],
                                                            invoice__invoice_type__in=stock_out_invoices).aggregate(
            total=Sum('main_unit_sub_warehouse'))
        if stock_out['total'] is None:
            stock_out['total'] = 0
        total = stock_in['total'] - stock_out['total']
        return total


    def sub_store_stock(self, store):
        stock_in_invoices = [4, 5, 16, 17]
        stock_out_invoices = [1, 2, 3, 6, 15, 17]
        stock_in = self.magedinvoiceitems_set.all().filter(invoice__sub_warehouse_id=store, invoice__deleted=False,
                                                           invoice__saved=True, item__product_type__in=[1, 2],
                                                           invoice__invoice_type__in=stock_in_invoices).aggregate(
            total=Sum('main_unit_sub_warehouse'))
        if stock_in['total'] is None:
            stock_in['total'] = 0

        stock_out = self.magedinvoiceitems_set.all().filter(invoice__sub_warehouse_id=store, invoice__deleted=False,
                                                            invoice__saved=True, item__product_type__in=[1, 2],
                                                            invoice__invoice_type__in=stock_out_invoices).aggregate(
            total=Sum('main_unit_sub_warehouse'))
        if stock_out['total'] is None:
            stock_out['total'] = 0
        total = stock_in['total'] - stock_out['total']
        return total


    def last_sell_date(self):
        invoice_item_set = self.invoiceitem_set.filter(invoice__invoice_type__in=[1, 2, 3]).order_by('invoice__date')
        if invoice_item_set.count() > 0:
            last_sold_invoice = invoice_item_set.last().invoice.date.date()
        else:
            last_sold_invoice = date.today().replace(year=1, month=1, day=1)
        return last_sold_invoice

    class Meta:
        ordering = ['id']
        default_permissions = ()
        permissions = (
            ('add_product', 'إضافة منتج'),
            ('edit_product', 'تعديل منتج'),
            ('delete_product', 'حذف منتج'),
            ('view_purchase_price', 'مشاهدة سعر الشراء'),
            ('view_cost_price', 'مشاهدة سعر التكلفة'),
            ('access_product_menu', 'الدخول علي قائمة المنتجات'),
        )


class ProductUnit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit_name = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True, related_name='unit_name', verbose_name='الوحدة')
    unit_quantity = models.FloatField(verbose_name='الكمية', default=1)
    unit_from = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True, related_name='unit_from', verbose_name='من وحدة')
    sell_price_factor = models.FloatField(default=0.0, verbose_name='معامل سعر البيع')
    purchase_price_factor = models.FloatField(default=0.0, verbose_name='معامل سعر الشراء')
    deleted = models.BooleanField(default=False, verbose_name='مسح')

    def __str__(self):
        return self.unit_name.name


class GroupedProduct(models.Model):
    grouped_item = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='المنتج المجمع',
                                     related_name='grouped_item')
    contain = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='المنتج', related_name='content')
    quantity = models.FloatField(default=0.0, verbose_name='الكمية')

    def __str__(self):
        return self.grouped_item.name


class ProductPrices(models.Model):
    op = (
        (1, '-'),
        (2, '+'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, verbose_name='اسم المنتج')
    customer_segment = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, verbose_name='الشريحة')
    price = models.FloatField(default=0.0, verbose_name='السعر')
    discount = models.FloatField(default=0.0, verbose_name='نسبة الخصم ')
    opration = models.IntegerField(choices=op, default=1 , verbose_name='العملية')
    new_price = models.FloatField(default=0.0, verbose_name='السعر بعد الخصم')
    order = models.IntegerField(default=1 , null=True, blank=True, verbose_name='الترتيب')
    last_update = models.DateTimeField(auto_now=True, verbose_name='آخر تحديث')
    deleted = models.BooleanField(default=False, verbose_name='مسح')
    inactive = models.BooleanField(default=False, verbose_name='تعطيل الشريحة')

    def __str__(self):
        return self.customer_segment.name

class CustomerPrices(models.Model):
    op = (
        (1, '-'),
        (2, '+'),
    )
    prices_list = models.ForeignKey(PricesList, on_delete=models.CASCADE, null=True, blank=True, verbose_name='اسم قائمة الاسعار')
    customer_segment = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, verbose_name='الشريحة')
    discount = models.FloatField(default=0.0, verbose_name='النسبة')
    opration = models.IntegerField(choices=op, default=1 , verbose_name='العملية')
    deleted = models.BooleanField(default=False, verbose_name='مسح')

    def __str__(self):
        return self.customer_segment.name


class ProductActions(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, verbose_name='اسم المنتج')
    action_time = models.DateTimeField(auto_now=True, verbose_name='وقت الحركة')
    action_userid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, verbose_name='الوظف')
    action_type = models.CharField(max_length=128, verbose_name='نوع الحركة')
    action_name = models.CharField(max_length=128, verbose_name='اسم الحركة')
    action_from = models.CharField(max_length=128, verbose_name='تغيير من')
    action_to = models.CharField(max_length=128, verbose_name='تغيير الي')

    def __str__(self):
        return self.product.name

