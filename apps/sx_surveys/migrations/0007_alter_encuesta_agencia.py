# Generated by Django 3.2.9 on 2024-01-11 23:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sx_surveys', '0006_encuesta_agencia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encuesta',
            name='agencia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sx_surveys.agencias'),
        ),
    ]
