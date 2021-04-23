# Generated by Django 2.2 on 2021-04-04 12:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=140, verbose_name='العنوان')),
                ('created_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='تاريخ الانشاء')),
                ('due_date', models.DateField(default=django.utils.timezone.now, null=True, verbose_name='موعد الانتهاء ')),
                ('completed', models.BooleanField(default=False, verbose_name='تم')),
                ('completed_date', models.DateField(blank=True, null=True, verbose_name='تاريخ الانتهاء')),
                ('message', models.TextField(blank=True, null=True, verbose_name='المحتوي')),
                ('deleted', models.BooleanField(default=False, verbose_name='حذف')),
                ('assigned_to_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.Group', verbose_name='موكلة الي مجموعة')),
                ('assigned_to_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='todo_assigned_to', to=settings.AUTH_USER_MODEL, verbose_name='موكلة الي شخص')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='todo_created_by', to=settings.AUTH_USER_MODEL, verbose_name='انشئ بواسطة')),
            ],
        ),
        migrations.CreateModel(
            name='TaskComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('comment', models.TextField(blank=True, verbose_name='الرسالة')),
                ('done_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='الناشر')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tasks.Task', verbose_name='المهمة')),
            ],
        ),
        migrations.CreateModel(
            name='TaskCommentSeenBy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('task_comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Tasks.TaskComment')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]