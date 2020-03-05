# Generated by Django 3.0.3 on 2020-03-02 08:37

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('p_library', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='friend',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='friend_books', to='p_library.Friend'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='borrow_date',
            field=models.DateField(default=datetime.datetime(2020, 3, 2, 8, 37, 0, 917111, tzinfo=utc), verbose_name='Дата с момента одолжения'),
        ),
    ]
