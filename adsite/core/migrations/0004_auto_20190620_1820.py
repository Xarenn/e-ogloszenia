# Generated by Django 2.2.1 on 2019-06-20 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_ad_is_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='category',
            field=models.CharField(choices=[('ELECTRONICS', 'ELECTRONICS')], default=None, max_length=64),
        ),
        migrations.AddField(
            model_name='ad',
            name='description',
            field=models.TextField(default=None, max_length=1024),
        ),
        migrations.AddField(
            model_name='ad',
            name='personality',
            field=models.CharField(choices=[('COMPANY', 'COMPANY')], default=None, max_length=64),
        ),
        migrations.AddField(
            model_name='ad',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='ad',
            name='short_description',
            field=models.CharField(default=None, max_length=120),
        ),
        migrations.AddField(
            model_name='ad',
            name='title',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AlterField(
            model_name='ad',
            name='is_featured',
            field=models.BooleanField(default=False, verbose_name='Is Fetaured'),
        ),
    ]
