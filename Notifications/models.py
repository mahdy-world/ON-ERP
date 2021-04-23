import datetime
from django.db import models
from Auth.models import User
from Tasks.models import Task

# Create your models here.
class Notification(models.Model):

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="noti_post", blank=True, null=True)
    title = models.CharField(max_length=128, verbose_name='العنوان')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_from_user" ,verbose_name='اضيف بواسطة')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_to_user", verbose_name='مرسلة الي')
    datetime = models.DateTimeField(auto_now_add=True , verbose_name='وقت الاضافة')
    content = models.TextField(null=True, blank='True',verbose_name='المحتوي')
    notification_type = models.CharField(max_length=128,verbose_name='نوع الرسالة')
    is_read = models.BooleanField(default=False , verbose_name='تم القرأة')

    def __str__(self):
        return self.title

class NotificationRed(models.Model):
    notifiaction = models.ForeignKey(Notification, related_name='created_notifications' , on_delete=models.SET_NULL , null=True , blank='True', verbose_name='الرسالة')
    datetime =  models.DateTimeField(auto_now_add=True , verbose_name = 'وقت الاضافة')  
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='اضيف بواسطة')      


