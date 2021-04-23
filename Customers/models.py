from django.db import models
from django.db.models import Count, Sum
from django.db.models import F, FloatField, Sum
from Auth.models import User
from django.db.models.signals import post_save, pre_save
from Technicians.models import Technician


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, verbose_name='الاسم')
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_customer_category', 'إضافة شريحة عملاء'),
            ('edit_customer_category', 'تعديل شريحة عملاء'),
            ('delete_customer_category', 'حذف شريحة عملاء'),
            ('access_customer_category_menu', 'الدخول علي قائمة شرائح العملاء'),
        )


class CustomerType(models.Model):
    name = models.CharField(max_length=128, verbose_name='الاسم')
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return self.name


class Customer(models.Model):
    color = (
        ('#FF0000', 'احمر'),
        ('#fff400', 'اصفر'),
        ('#00c33e', 'اخضر'),
    )
    name = models.CharField(max_length=128, verbose_name='الاسم')
    phone = models.CharField(max_length=14, null=True, blank=True, verbose_name='الموبايل')
    address = models.TextField(null=True, blank=True, verbose_name='العنوان')
    technician = models.ForeignKey(Technician, on_delete=models.SET_NULL, null=True, blank=True ,verbose_name='الفني الافتراضي')
    payments_status = models.CharField(default="#00c33e",choices=color , max_length=50, verbose_name='حالة الدفعات', null=True, blank=True)
    Products_status = models.CharField(default="#00c33e", choices=color , max_length=50, verbose_name='حالة المنتجات', null=True, blank=True)
    seller_feedback = models.TextField(null=True, blank=True, verbose_name='ملاحظات البائع')
    accountant_notes = models.TextField(null=True, blank=True, verbose_name='ملاحظات المحاسب')
    secret = models.BooleanField(default=False, verbose_name='سري')
    customer_type = models.ForeignKey(CustomerType, on_delete=models.SET_NULL, null=True, blank='True',
                                      verbose_name='نوع العميل')
    facebook_account = models.CharField(max_length=128, verbose_name='حساب الفيس بوك', null=True, blank=True)
    job = models.CharField(max_length=128, null=True, blank=True, verbose_name='مجموعه فرعيه')
    sales_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,
                                       verbose_name='شريحة المبيعات', related_name='customers_category')
    purchases_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,
                                           verbose_name='شريحة المشتريات', related_name='vendors_category')
    initial_balance = models.FloatField(default=0, verbose_name='الرصيد الافتتاحي')
    allow_negative_balance = models.BooleanField(default=False, verbose_name='السماح بالبيع آجل')
    max_negative_balance = models.FloatField(default=0, verbose_name='الحد الإئتماني')
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='اضيف بواسطة')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='أضيف بتاريخ')
    main_account = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name='الحساب الرئيسي')
    administrator = models.CharField(max_length=128, verbose_name='المسئول', null=True, blank=True)
    purchase_invoices_comments = models.TextField(verbose_name='ملاحظات بفاتوره المشتريات', null=True, blank=True)
    deleted = models.BooleanField(default=False, verbose_name='حذف')
     
    def __str__(self):
        return self.name

    def balance(self):
        invoices = self.invoice_set.filter(deleted=False, saved=True)
        balance = invoices.aggregate(
            total=Sum(F('customer_debit'), output_field=FloatField()) - Sum(F('customer_credit'),
                                                                            output_field=FloatField()),
            debit=Sum('customer_debit'), credit=Sum('customer_credit'))
        if not balance['total']:
            return self.initial_balance
        else:
            return balance['total'] + self.initial_balance

    def total_debit(self):
        invoices = self.invoice_set.filter(deleted=False, saved=True)
        balance = invoices.aggregate(debit=Sum('customer_debit'))
        if self.initial_balance > 0:
            if not balance['debit']:
                return self.initial_balance
            else:
                return balance['debit'] + self.initial_balance
        else:
            if not balance['debit']:
                return 0
            else:
                return balance['debit']

    def total_credit(self):
        invoices = self.invoice_set.filter(deleted=False, saved=True)
        balance = invoices.aggregate(credit=Sum('customer_credit'))
        if self.initial_balance < 0:
            if not balance['credit']:
                return self.initial_balance
            else:
                return balance['credit'] - self.initial_balance
        else:
            if not balance['credit']:
                return 0
            else:
                return balance['credit']

    def is_creditor(self):
        if self.balance():
            if self.balance() < 0:
                return True
            else:
                return False

    def is_debitor(self):
        if self.balance():
            if self.balance() > 0:
                return True
            else:
                return False

    def sales_invoices(self):
        return self.invoice_set.filter(deleted=False, invoice_type=1)

    def quotations(self):
        return self.invoice_set.filter(deleted=False, invoice_type=7)


     
    
    class Meta:
        ordering = ['id']
        default_permissions = ()
        permissions = (
            ('add_customer', 'إضافة عميل/مورد'),
            ('edit_customer', 'تعديل عميل/مورد'),
            ('delete_customer', 'حذف عميل/مورد'),
            ('view_customer', 'عرض بيانات عميل/مورد'),
            ('view_customer_balance', 'عرض رصيد عميل/مورد'),
            ('view_customer_statement', 'كشف حساب عميل/مورد'),
            ('access_customer_menu', 'الدخول علي قائمة العملاء/الموردين'),
        )

       
    
class CustomerNote(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, verbose_name='العميل')
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='الموظف')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='التاريخ')
    title = models.CharField(max_length=128, verbose_name='عنوان الملاحظات')
    note = models.TextField(verbose_name='محتوي الملاحظة')

    def __str__(self):
        return self.title


class CallReason(models.Model):
    name = models.CharField(verbose_name='سبب الإتصال', max_length=128)
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return self.name


class CustomerCall(models.Model):
    call_type_choices = (
        (1, 'مكالمة صادرة'),
        (2, 'مكالمة واردة'),
        (3, 'Whatsapp'),
        (4, 'Messenger')
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, verbose_name='العميل')
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='الموظف')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='التاريخ')
    call_type = models.IntegerField(choices=call_type_choices, verbose_name='نوع المكالمة')
    call_reason = models.ForeignKey(CallReason, on_delete=models.SET_NULL, null=True, verbose_name='سبب المكالمة')
    summary = models.TextField(verbose_name='ملخص المكالمة')

    def __str__(self):
        return self.summary


class CustomerHistory(models.Model):
    history_type_choices = (
        (1, 'إضافة عميل'),
        (2, 'إضافة مكالمة'),
        (3, 'إضافة عرض سعر'),
        (4, 'إضافة فاتورة مبيعات'),
        (5, 'إضافة فاتورة مرتجع مبيعات'),
        (6, 'إضافة فاتورة مشتريات'),
        (7, 'إضافة فاتورة مرتجع مشتريات'),
        (8, 'إضافة ملاحظة'),
        (9, 'إضافة مكالمة'),
        (10, 'تحديد مهام'),
    )
    history_type = models.IntegerField(choices=history_type_choices, verbose_name='نوع العملية')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, verbose_name='العميل')
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='الموظف')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='التاريخ')
    call = models.ForeignKey(CustomerCall, on_delete=models.CASCADE, verbose_name='المكالمة', null=True)
    note = models.ForeignKey(CustomerNote, on_delete=models.CASCADE, verbose_name='الملاحظة', null=True)
    invoice_id = models.IntegerField(verbose_name='رقم الفاتورة', null=True)

    def __str__(self):
        return self.get_history_type_display()

    class Meta:
        ordering = ['-added_at']


def save_customer(sender, instance, created, **kwargs):
    if created:
        history = CustomerHistory()
        history.added_by = instance.added_by
        history.added_at = instance.added_at
        history.history_type = 1
        history.customer = instance
        history.save()


post_save.connect(save_customer, sender=Customer)


class Pricing(models.Model):
    name = models.CharField(max_length=128, verbose_name='اسم السعر')

    def __str__(self):
        return self.name


