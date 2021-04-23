from django.db import models
from Auth.models import User


# Create your models here.
class Technician(models.Model):
    name = models.CharField(max_length=128, verbose_name='الاسم')
    phone = models.CharField(max_length=11, verbose_name='رقم التليفون', default='0')
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='أضيف بواسطة')
    added_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return self.name


