# Generated by Django 3.1.2 on 2021-09-15 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20210915_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='almacenpoint',
            name='markermodel',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='tiendapoint',
            name='markermodel',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
