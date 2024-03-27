# Generated by Django 3.2.9 on 2024-01-11 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sx_surveys', '0003_alter_encuesta_programacion_cita'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agencias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
            ],
        ),
        migrations.AddField(
            model_name='encuesta',
            name='numero_orden',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
