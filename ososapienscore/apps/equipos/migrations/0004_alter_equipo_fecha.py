# Generated by Django 5.0.6 on 2024-05-27 10:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipos', '0003_alter_equipo_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipo',
            name='fecha',
            field=models.TimeField(default=datetime.datetime(2024, 5, 27, 10, 29, 12, 420798, tzinfo=datetime.timezone.utc)),
        ),
    ]
