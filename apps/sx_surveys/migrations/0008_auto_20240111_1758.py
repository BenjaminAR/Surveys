# Generated by Django 3.2.9 on 2024-01-11 23:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sx_surveys', '0007_alter_encuesta_agencia'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agencias',
            options={'verbose_name': 'Agencia', 'verbose_name_plural': 'Agencias'},
        ),
        migrations.AlterModelOptions(
            name='encuesta',
            options={'verbose_name': 'Encuesta', 'verbose_name_plural': 'Encuestas'},
        ),
    ]
