# Generated by Django 3.2.9 on 2024-01-11 09:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sx_surveys', '0004_auto_20240111_0242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encuesta',
            name='fecha',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
