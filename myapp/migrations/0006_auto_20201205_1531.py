# Generated by Django 3.1.3 on 2020-12-05 20:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20201205_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 12, 5, 20, 31, 46, 73885, tzinfo=utc), max_length=50),
        ),
    ]
