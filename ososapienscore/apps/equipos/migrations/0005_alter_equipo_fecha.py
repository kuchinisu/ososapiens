# Generated by Django 5.0.6 on 2024-05-28 07:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipos', '0004_alter_equipo_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipo',
            name='fecha',
            field=models.TimeField(default=datetime.datetime(2024, 5, 28, 7, 56, 44, 475370, tzinfo=datetime.timezone.utc)),
        ),
    ]