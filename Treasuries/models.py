from django.db import models
from Branches.models import Branch


# Create your models here.
class Treasury(models.Model):
    types = (
        (1, 'خزينة'),
        (2, 'حساب بنكي'),
        (3, 'حساب عهدة'),
        (4, 'حساب سلف رواتب'),
        (5, 'حاقظة اوراق دفع'),
        (6, 'حاقظة اوراق قبض'),
    )
    type = models.IntegerField(choices=types, verbose_name='النوع')
    name = models.CharField(max_length=128, verbose_name='الاسم')
    no = models.CharField(max_length=128, verbose_name='رقم الحساب', null=True, blank=True)
    initial_balance = models.FloatField(default=0, verbose_name='الرصيد الافتتاحي')
    branch = models.ForeignKey(Branch ,related_name='branch_treasuires', on_delete=models.SET_NULL, null=True, blank='True' , verbose_name='الفرع المرتبط' )
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def balance(self):
        in_invoices = self.treasury_in_transactions.filter(saved=True, deleted=False)
        out_invoices = self.treasury_out_transactions.filter(saved=True, deleted=False)
        balance = self.initial_balance
        for invoice in in_invoices:
            balance += invoice.treasury_in
        for invoice in out_invoices:
            balance -= invoice.treasury_out
        return balance

class PaymentMachines(models.Model):
    name = models.CharField(max_length=200, verbose_name='الاسم')
    discount_percentage = models.FloatField(default=0, verbose_name='نسبة الخصم')
    transfer = models.ForeignKey(Treasury , on_delete=models.SET_NULL, max_length=128, verbose_name='لتحويل الى', null=True, blank=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
         return self.name
