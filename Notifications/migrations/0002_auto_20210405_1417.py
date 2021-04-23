# Generated by Django 2.2 on 2021-04-05 12:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Tasks', '0002_auto_20210405_1255'),
        ('Notifications', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='receiver',
        ),
        migrations.AddField(
            model_name='notification',
            name='sender',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='noti_from_user', to=settings.AUTH_USER_MODEL, verbose_name='اضيف بواسطة'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='noti_post', to='Tasks.Task'),
        ),
        migrations.AddField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='noti_to_user', to=settings.AUTH_USER_MODEL, verbose_name='مرسلة الي'),
            preserve_default=False,
        ),
    ]
