# Generated by Django 2.2 on 2021-04-04 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('HR', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobtitle',
            name='group',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.Group', verbose_name='المسمي الوظيفي'),
        ),
    ]
