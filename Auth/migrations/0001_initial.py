# Generated by Django 2.2 on 2021-04-04 12:19

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('Treasuries', '0001_initial'),
        ('Branches', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='', verbose_name='صورة البروفايل')),
                ('allowed_branches', models.ManyToManyField(blank=True, to='Branches.Branch', verbose_name='الفروع المتاحة')),
                ('allowed_treasuries', models.ManyToManyField(blank=True, to='Treasuries.Treasury', verbose_name='الخزائن المتاحة')),
                ('default_branch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='default_branch', to='Branches.Branch', verbose_name='الفرع الافتراضي')),
                ('default_treasury', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='default_treasury', to='Treasuries.Treasury', verbose_name='الخزينة الافتراضية')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'permissions': (('add_user', 'إضافة موظف'), ('edit_user', 'تعديل موظف'), ('delete_user', 'حذف موظف'), ('view_user', 'عرض بيانات موظف'), ('edit_user_permissions', 'تعديل صلاحيات موظف'), ('access_user_menu', 'الدخول علي قائمة الموظفين')),
                'default_permissions': (),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
