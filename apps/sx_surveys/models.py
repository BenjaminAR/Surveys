# models.py
from django.utils import timezone
from django.db import models
from datetime import timedelta

class Agencias(models.Model):
    nombre = models.CharField(max_length=150)

    class Meta:
        verbose_name='Agencia'
        verbose_name_plural='Agencias'
    
    def __str__(self):
        return f"  {self.nombre}"

def default_fecha():
    return timezone.now() - timedelta(hours=6)

class Encuesta(models.Model):
    #Datos de control
    fecha = models.DateTimeField(default=default_fecha)
    numero_orden = models.IntegerField()
    agencia = models.ForeignKey(Agencias, on_delete=models.CASCADE, null=False, blank=False)
    #Cliente experiencia
    vivio_experiencia_completa = models.BooleanField()
    tipo_servicio = models.CharField(max_length=255)
    recomendar_mitsubishi = models.IntegerField()
    razones_recomendacion = models.TextField()
    #Servicio "La programacion de cita debe ir con Entrega"
    programacion_cita = models.CharField(max_length=255)
    calificacion_programacion_cita = models.IntegerField()
    obtener_cita_deseada = models.BooleanField()
    calificacion_servicio_general = models.IntegerField()
    #Asesor
    tiempo_espera_asesor = models.CharField(max_length=255)
    acciones_asesor = models.CharField(max_length=350)
    calificacion_atencion_asesor = models.IntegerField()
    #Instalaciones
    ofrecieron_cortesias = models.BooleanField()
    calificacion_instalaciones = models.IntegerField()
    #Entrega
    vehiculo_entregado_prometido = models.BooleanField()
    costo_final_coincide_presupuesto = models.CharField(max_length=255)
    explicacion_reparaciones = models.BooleanField()
    limpieza_vehiculo = models.BooleanField()
    calificacion_entrega_general = models.IntegerField()

    def fecha_texto(self):
        return self.fecha.strftime('%d/%m/%Y')

    def vivio_experiencia_completa_texto(self):
        return "Si" if self.vivio_experiencia_completa else "No"
    
    def vehiculo_entregado_prometido_texto(self):
        return "Si" if self.vehiculo_entregado_prometido else "No"
    
    #explicacion_reparaciones
    def explicacion_reparaciones_texto(self):
        return "Si" if self.explicacion_reparaciones else "No"

    #limpieza_vehiculo
    def limpieza_vehiculo_texto(self):
        return "Si" if self.limpieza_vehiculo else "No"
    #ofrecieron_cortesias
    def ofrecieron_cortesias_texto(self):
        return "Si" if self.ofrecieron_cortesias else "No"

    def obtener_cita_deseada_texto(self):
        return "Si" if self.obtener_cita_deseada else "No"
    
    def acciones_asesor_con_saltos_de_linea(self):
        print(type(self.acciones_asesor))
        acciones_asesor_n = self.acciones_asesor.replace('.', '. \n')
        print(acciones_asesor_n)
        return acciones_asesor_n

    class Meta:
        verbose_name='Encuesta'
        verbose_name_plural='Encuestas'

    def __str__(self):
        return f"Encuesta de la orden:  {self.numero_orden}"
