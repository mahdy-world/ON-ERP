from django.db import models


# Create your models here.
class Branch(models.Model):
    name = models.CharField(max_length=128, verbose_name='الاسم')
    address = models.CharField(max_length=128, verbose_name='العنوان', null=True, blank=True)
    phone = models.CharField(max_length=128, verbose_name='التليفون', null=True, blank=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        default_permissions = ()
        permissions = (
            ('add_branch', 'إضافة فرع'),
            ('edit_branch', 'تعديل فرع'),
            ('delete_branch', 'حذف فرع'),
            ('access_branch_menu', 'الدخول علي قائمة الفروع'),
        )


class Warehouse(models.Model):
    name = models.CharField(max_length=128, verbose_name='اسم المخزن')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='الفرع')
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_warehouse', 'إضافة مخزن'),
            ('edit_warehouse', 'تعديل مخزن'),
            ('delete_warehouse', 'حذف مخزن'),
            ('access_warehouse_menu', 'الدخول علي قائمة المخازن'),
        )


class BranchWarehouses(models.Model):
    branch = models.OneToOneField(Branch, on_delete=models.CASCADE, verbose_name='الفرع')
    main_warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=True,
                                       verbose_name='المخزن الرئيسي', related_name='main_warehouse_set')
    sub_warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=True,
                                      verbose_name='المخزن الفرعي', related_name='sub_warehouse_set')

    def __str__(self):
         return self.branch.name



