# Generated by Django 2.2.1 on 2019-05-17 11:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='entry_date',
            field=models.DateField(default=datetime.date(2019, 5, 17)),
        ),
    ]