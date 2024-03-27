# Generated by Django 3.2.9 on 2023-12-08 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Encuesta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('vivio_experiencia_completa', models.BooleanField()),
                ('tipo_servicio', models.CharField(max_length=255)),
                ('recomendar_mitsubishi', models.IntegerField()),
                ('razones_recomendacion', models.TextField()),
                ('programacion_cita', models.IntegerField()),
                ('calificacion_programacion_cita', models.IntegerField()),
                ('obtener_cita_deseada', models.BooleanField()),
                ('calificacion_servicio_general', models.IntegerField()),
                ('tiempo_espera_asesor', models.CharField(max_length=255)),
                ('acciones_asesor', models.CharField(max_length=255)),
                ('calificacion_atencion_asesor', models.IntegerField()),
                ('ofrecieron_cortesias', models.IntegerField()),
                ('calificacion_instalaciones', models.IntegerField()),
                ('vehiculo_entregado_prometido', models.BooleanField()),
                ('costo_final_coincide_presupuesto', models.CharField(max_length=255)),
                ('explicacion_reparaciones', models.BooleanField()),
                ('limpieza_vehiculo', models.BooleanField()),
                ('calificacion_entrega_general', models.IntegerField()),
            ],
        ),
    ]
