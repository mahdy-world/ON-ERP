import django.contrib.auth.models
from django.db import models
from django.contrib.auth.models import Group
from Auth.models import User 

from django.utils.timezone import now
import os
import textwrap

 



# Create your models here.

class Task(models.Model):
    color = (
        ('#FF0000', 'احمر'),
        ('#fff400', 'اصفر'),
        ('#00c33e', 'اخضر'),
    )
    title = models.CharField(max_length=140,verbose_name='العنوان')
    created_date = models.DateField(default=now, blank=True, null=True,verbose_name='تاريخ الانشاء')
    due_date = models.DateField(default=now , null=True, verbose_name='موعد الانتهاء ' )
    completed = models.BooleanField(default=False , verbose_name='تم')
    completed_date = models.DateField(blank=True, null=True , verbose_name='تاريخ الانتهاء')
    created_by = models.ForeignKey(User,null=True,blank=True,related_name="todo_created_by",on_delete=models.CASCADE,verbose_name='انشئ بواسطة')
    assigned_to_user = models.ForeignKey( User, blank=True,null=True,related_name="todo_assigned_to",on_delete=models.CASCADE,verbose_name='موكلة الي شخص')
    assigned_to_group = models.ForeignKey(Group, on_delete=models.CASCADE,blank=True,null=True,verbose_name='موكلة الي مجموعة')
    message = models.TextField(verbose_name='المحتوي' , null=False , blank=False )
    priority = models.CharField(default="#00c33e",choices=color , max_length=50, verbose_name='الأولوية')
   
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return self.message

    def is_overdue(self):
        if not self.completed:
            if self.created_date:
                if now().date() > self.created_date:
                    return True

    def is_today(self):
        if not self.completed:
            if self.created_date:
                if now().date() == self.created_date:
                    return True    
    

class TaskComment(models.Model):
    done_by = models.ForeignKey( User, on_delete=models.CASCADE, blank=True, null=True , verbose_name='الناشر')
    task = models.ForeignKey(Task, on_delete=models.CASCADE , verbose_name='المهمة')
    created_date = models.DateTimeField(auto_now=True)
    comment = models.TextField(blank=True,verbose_name='الرسالة')

    def __str__(self):
        return self.comment


class TaskCommentSeenBy(models.Model):
    task_comment = models.ForeignKey(TaskComment, on_delete=models.CASCADE , blank=True, null=True)
    user = models.ForeignKey( User, on_delete=models.CASCADE, blank=True, null=True )
    timestamp = models.DateField(default=now, blank=True, null=True)
