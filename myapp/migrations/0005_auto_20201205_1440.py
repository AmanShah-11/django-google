# Generated by Django 3.1.3 on 2020-12-05 19:40

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20201205_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 12, 5, 19, 40, 29, 130656, tzinfo=utc), max_length=50),
        ),
    ]
