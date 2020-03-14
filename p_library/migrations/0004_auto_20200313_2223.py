# Generated by Django 3.0.3 on 2020-03-13 12:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('p_library', '0003_auto_20200308_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='photo',
            field=models.ImageField(blank=True, upload_to='books/photo'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='borrow_date',
            field=models.DateField(default=datetime.datetime(2020, 3, 13, 12, 23, 11, 288728, tzinfo=utc), verbose_name='Дата с момента одолжения'),
        ),
    ]
