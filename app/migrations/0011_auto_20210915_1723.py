# Generated by Django 3.1.2 on 2021-09-15 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20210915_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='almacenpoint',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='tiendapoint',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]