from django.db import models
from Auth.models import User
from django.contrib.auth.models import Group


# Create your models here.
class Employee(models.Model):
    id_types = (
        (1, 'بطاقة رقم قومي'),
        (2, 'جواز سفر'),
    )
    religion_choices = (
        (1, 'مسلم'),
        (2, 'مسيحي'),
        (3, 'يهودي'),
    )
    social_state_choices = (
        (1, 'أعزب'),
        (2, 'خاطب'),
        (3, 'متزوج'),
        (4, 'مطلق'),
        (5, 'أرمل')
    )
    military_state_choices = (
        (1, 'معفي نهائي'),
        (2, 'معفي مؤقت'),
        (3, 'أتم فترة التجنيد'),
    )
    employee_types = (
        (1, 'متقدم لوظيفة'),
        (2, 'موظف مؤقت'),
        (3, 'موظف دائم'),
    )
    name = models.CharField(max_length=1024, verbose_name='الاسم بالكامل')
    image = models.ImageField(null=True, blank=True, verbose_name='الصورة الشخصية')
    phone = models.CharField(max_length=14, null=True, blank=True, verbose_name='الهاتف')
    address = models.CharField(max_length=128, null=True, blank=True, verbose_name='العنوان')
    birthday = models.DateField(null=True, blank=True, verbose_name='تاريخ الميلاد')
    email = models.EmailField(null=True, blank=True, verbose_name='البريد الالكتروني')
    qualification = models.CharField(max_length=128, null=True, blank=True, verbose_name='المؤهل')
    id_type = models.IntegerField(choices=id_types, null=True, blank=True, verbose_name='نوع تحقيق الشخصية')
    national_id = models.CharField(max_length=28, null=True, blank=True, verbose_name='رقم تحقيق الشخصية')
    id_issued_from = models.CharField(max_length=128, null=True, blank=True, verbose_name='جهة إصدار تحقيق الشخصية')
    settlement_end_date = models.DateField(null=True, blank=True, verbose_name='انتهاء الاقامة/تحقيق الشخصية')
    salary = models.FloatField(null=True, blank=True, verbose_name='الراتب')
    over = models.FloatField(null=True, blank=True, verbose_name='الحافز')
    insurance_start = models.DateField(null=True, blank=True, verbose_name='تاريخ التأمين')
    insurance_end = models.DateField(null=True, blank=True, verbose_name='تاريخ الانتهاء')
    insurance_cost = models.FloatField(null=True, blank=True, verbose_name='تكلفة التأمينات')
    finger_print_id = models.IntegerField(null=True, blank=True, verbose_name='الرقم علي جهاز البصمة')
    start_date = models.DateField(null=True, blank=True, verbose_name='تاريخ التعيين')
    end_date = models.DateField(null=True, blank=True, verbose_name='تاريخ انتهاء العقد')
    religion = models.IntegerField(choices=religion_choices, null=True, blank=True, verbose_name='الديانة')
    military_state = models.IntegerField(choices=military_state_choices, null=True, blank=True, verbose_name='موقف التجنيد')
    relationship = models.IntegerField(choices=social_state_choices, null=True, blank=True, verbose_name='الحالة الاجتماعية')
    rest_credit = models.IntegerField(null=True, blank=True, verbose_name='رصيد الإجازات')
    weekly_rest_days = models.IntegerField(null=True, blank=True, verbose_name='أيام الاجازة الاسبوعية')
    monthly_rest_days = models.IntegerField(null=True, blank=True, verbose_name='أيام الاجازة الشهرية')
    yearly_rest_days = models.IntegerField(null=True, blank=True, verbose_name='أيام الاجازة السنوية')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='حساب البرنامج')
    employee_type = models.IntegerField(choices=employee_types, null=True, blank=True, verbose_name='نوع الموظف')
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return self.name


class EmployeeFile(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='الموظف')
    file = models.FileField(verbose_name='الملف')

    def __str__(self):
        return self.file.name


