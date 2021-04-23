

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Technicians', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='technician',
            name='phone',
            field=models.CharField(default='0', max_length=11, verbose_name='رقم التليفون'),
        ),
    ]
