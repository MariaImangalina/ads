# Generated by Django 3.0.6 on 2020-12-02 09:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20201124_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='expiration_date',
            field=models.DateField(default=datetime.date(2020, 12, 1)),
        ),
    ]