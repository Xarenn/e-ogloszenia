# Generated by Django 2.2.1 on 2019-06-19 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='is_active',
            field=models.CharField(choices=[('T', 'T'), ('F', 'F')], default='F', max_length=1),
        ),
        migrations.AddField(
            model_name='ad',
            name='server_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]