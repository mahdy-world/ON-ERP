# Generated by Django 2.2 on 2021-04-04 12:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='العنوان')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='وقت الاضافة')),
                ('content', models.TextField(blank='True', null=True, verbose_name='المحتوي')),
                ('notification_type', models.CharField(max_length=128, verbose_name='نوع الرسالة')),
                ('is_read', models.BooleanField(default=False, verbose_name='تم القرأة')),
                ('receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='اضيف بواسطة')),
            ],
        ),
        migrations.CreateModel(
            name='NotificationRed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='وقت الاضافة')),
                ('notifiaction', models.ForeignKey(blank='True', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_notifications', to='Notifications.Notification', verbose_name='الرسالة')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='اضيف بواسطة')),
            ],
        ),
    ]
