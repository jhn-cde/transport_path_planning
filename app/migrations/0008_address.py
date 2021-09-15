# Generated by Django 3.1.2 on 2021-09-15 16:30

from django.db import migrations, models
import djgeojson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_polygonlayer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', djgeojson.fields.PointField()),
            ],
        ),
    ]
