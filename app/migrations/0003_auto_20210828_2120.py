# Generated by Django 3.2.6 on 2021-08-29 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210828_2109'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bodega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200, null=True)),
                ('lat', models.FloatField(null=True)),
                ('lng', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tienda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200, null=True)),
                ('lat', models.FloatField(null=True)),
                ('lng', models.FloatField(null=True)),
                ('zone', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Search',
        ),
    ]
