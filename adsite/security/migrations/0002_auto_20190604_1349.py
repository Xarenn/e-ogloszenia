# Generated by Django 2.2.1 on 2019-06-04 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='server_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
