# models.py
from django.utils import timezone
from django.db import models
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as gl_
import re

def validate_no_special_characters(value):
    if not value:
        raise ValidationError('El valor no puede estar vacío.')
    
    # Define una expresión regular para permitir solo caracteres alfanuméricos y espacios
    pattern = re.compile(r'^[a-zA-Z0-9\s,.ñÑ@]+$')
    
    if not pattern.match(value):
        raise ValidationError('El valor no puede contener caracteres especiales como: = , \' " {} [] () % $ #')

def validate_no_sql_injection(value):
    # Palabras clave comunes utilizadas en inyección SQL
    sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'UNION', 'OR']

    # Verifica si el valor contiene alguna palabra clave de SQL
    for keyword in sql_keywords:
        if keyword in value.upper():
            raise ValidationError('Se ha detectado un intento de inyección SQL.')

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
    #Datos personales cliente
    nombre_cliente = models.CharField(max_length=255, default=None, null=True, blank=False)
    numero_telefono = models.CharField(max_length=19, default=None, null=True, blank=False)
    correo_cliente = models.EmailField(max_length=254, default=None, null=True, blank=False)
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

    def numero_telefono_text(self):
        if self.phone_number is not None:
            if not self.numero_telefono.isdigit():
                raise ValidationError(
                    gl_("%(value)s No es un numero valido"),
                    params={"value": self.phone_number},
                )    
        return self.numero_telefono.strip() if self.numero_telefono else None
    
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
        verbose_name= f'Encuesta Mitsubishi'
        verbose_name_plural='Encuestas Mitsubishi'

    def __str__(self):
        return f"Encuesta de la orden:  {self.numero_orden} y agencia: {self.agencia}"

class Encuesta_automotores(models.Model):
    #Control de la entrada
    
    fecha = models.DateTimeField(default=default_fecha,)
    
    numero_orden = models.PositiveSmallIntegerField()
    
    agencia = models.ForeignKey(Agencias, on_delete=models.CASCADE, null=False, blank=False)
    #Datos de el cliente
    
    nombre_cliente = models.CharField(max_length=255, default=None, null=True, blank=False)
    
    numero_telefono = models.CharField(max_length=19, default=None, null=True, blank=False,)
    
    correo_cliente = models.EmailField(max_length=254, default=None, null=True, blank=False, )
 
    #1

    recomendar_a_familiares_amigos = models.PositiveSmallIntegerField(verbose_name="¿Qué tan probable es que recomiende a Automotores de México a sus familiares y amigos?", help_text="Calificación del 1 al 10", )
    #2
    
    tipo_trabajo_realizado = models.CharField(max_length=255, verbose_name="¿Qué tipo de trabajo le fue realizado a su vehículo?", help_text="Seleccione todas las opciones que correspondan", )
    #3
    
    programacion_cita = models.PositiveSmallIntegerField(verbose_name="¿Cómo califica el proceso para programar su cita al taller de servicio?", help_text="Calificación del 1 al 10", )
    #4
    
    sacar_cita_deseada = models.BooleanField(verbose_name="¿Pudo sacar una cita el día/hora que usted quiso?", )
    #5
    
    como_programo_visita_servicio = models.CharField(max_length=255, verbose_name="¿Cómo programó esta visita de servicio?", )
    #6
    
    apoyo_transporte_alternativo = models.CharField(max_length=255, verbose_name="¿Se le ofreció apoyo para solicitar transporte alternativo?", )
    #7
    
    calificacion_instalaciones_amenidades = models.PositiveSmallIntegerField(verbose_name="¿Cómo evalúa las instalaciones del distribuidor y las amenidades ofrecidas?", help_text="Calificación del 1 al 10", )
    #8
    
    capacidad_asesor_entender_necesidades = models.PositiveSmallIntegerField(verbose_name="¿Cómo califica la capacidad del asesor para entender sus necesidades y responder a sus preguntas?", help_text="Calificación del 1 al 10", )
    #9
    
    calificacion_asesor_general = models.PositiveSmallIntegerField(verbose_name="¿Cómo evalúa a su asesor de servicio en general?", help_text="Calificación del 1 al 10", )
    #10
    
    mantener_informado_estado_vehiculo = models.BooleanField(verbose_name="¿El asesor de servicio le mantuvo informado del estado de su vehículo durante su visita al taller?", )
    #11
    
    detalle_explicaciones_asesor = models.PositiveSmallIntegerField(verbose_name="¿Cómo califica el detalle de las explicaciones que su asesor de servicio le brindó?", help_text="Calificación del 1 al 10", )
    #12
    
    capacidad_asesor_generar_confianza = models.PositiveSmallIntegerField(verbose_name="¿Cómo califica la capacidad del asesor para generar confianza con respecto al servicio prestado?", help_text="Calificación del 1 al 10", )
    #13
    
    trabajo_completado_primera = models.BooleanField(verbose_name="¿El trabajo fue completado bien y a la primera?", )
    #14
    
    motivo_trabajo_no_completado_primera = models.CharField(max_length=255, default=None, blank=True, null=True, verbose_name="NO = ¿Por qué considera que los trabajos solicitados no fueron realizados bien y a la primera?", help_text="Seleccione una opción si el trabajo no fue completado bien y a la primera", )
    #15 
    
    condiciones_vehiculo_despues_trabajo = models.PositiveSmallIntegerField(verbose_name="¿Cómo califica las condiciones del vehículo después del trabajo realizado, con respecto al estado original?", help_text="Calificación del 1 al 10", )
    #16
    
    limpieza_vehiculo_devolucion = models.PositiveSmallIntegerField(verbose_name="¿Cómo califica la limpieza del vehículo en la devolución?", help_text="Calificación del 1 al 10", )
    #17
    
    llamada_cortesia_despues_entrega_vehiculo = models.BooleanField(verbose_name="¿Recibió una llamada de cortesía de su distribuidor unos días después de la entrega de su vehículo?", )
    #18
    
    vehiculo_listo_hora_acordada = models.BooleanField(verbose_name="¿El vehículo estuvo listo a la hora acordada?", )
    #19
    
    personal_distribuidor_valoro_tiempo = models.BooleanField(verbose_name="¿Considera que el personal del distribuidor valoró su tiempo, durante su visita al taller?", )
    
    # Otras definiciones de métodos y clases aquí
    def fecha_formateada(self):
        return self.fecha.strftime('%d/%m/%Y')

    def sacar_cita_deseada_texto(self):
        return "Si" if self.sacar_cita_deseada else "No"
    
    def mantener_informado_estado_vehiculo_texto(self):
        return "Si" if self.mantener_informado_estado_vehiculo else "No"    
    
    def trabajo_completado_primera_texto(self):
        return "Si" if self.trabajo_completado_primera else "No"     
    
    def llamada_cortesia_despues_entrega_vehiculo_texto(self):
        return "Si" if self.llamada_cortesia_despues_entrega_vehiculo else "No"     
        
    def vehiculo_listo_hora_acordada_texto(self):
        return "Si" if self.vehiculo_listo_hora_acordada else "No"     
        
    def personal_distribuidor_valoro_tiempo_texto(self):
        return "Si" if self.personal_distribuidor_valoro_tiempo else "No" 
   
    def motivo_trabajo_no_completado_primera_texto(self):
        return 'No aplica' if self.trabajo_completado_primera_texto() == "Si"  else self.motivo_trabajo_no_completado_primera
    
    class Meta:
        verbose_name='Encuesta AMSA'
        verbose_name_plural='Encuestas AMSA'

    def __str__(self):
        return f"Encuesta de la orden:  {self.numero_orden} y agencia: {self.agencia}"