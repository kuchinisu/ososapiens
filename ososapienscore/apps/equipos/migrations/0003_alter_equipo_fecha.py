# Generated by Django 5.0.6 on 2024-05-25 01:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipos', '0002_alter_equipo_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipo',
            name='fecha',
            field=models.TimeField(default=datetime.datetime(2024, 5, 25, 1, 58, 33, 873378, tzinfo=datetime.timezone.utc)),
        ),
    ]