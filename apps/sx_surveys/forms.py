# forms.py
from django import forms
from .models import Encuesta
from .widgets import *
from django.utils import timezone


class EncuestaFormMitsu(forms.ModelForm):

    class Meta:
        model = Encuesta
        fields = '__all__'  # Incluye todos los campos del modelo en el formulario

    TIPO_SERVICIO_VEHICULO = [
        ('Servicio preventivo', 'Servicio preventivo'),
        ('Servicio correctivo','Servicio correctivo'),
        ('Hojalatería y pintura', 'Hojalatería y pintura'),
        ('Garantía auto nuevo', 'Garantía auto nuevo'),
        ('Otro','Otro'),

    ]
    
    COSTO_FINAL_CHOICES = [
        ('Sí', 'Sí'),
        ('No, el costo real fue menor que el presupuesto', 'No, el costo real fue menor que el presupuesto'),
        ('No, el costo real fue mayor que el presupuesto', 'No, el costo real fue mayor que el presupuesto'),
    ]
    
    PROGRAMACION_CITA_SERVICIO_CHOICES = [
        ('1.- Llamé para solicitar una cita', '1.- Llamé para solicitar una cita'),
        ('2.- Programé una cita por Internet', '2.- Programé una cita por Internet'),
        ('3.- Programé una cita vía mensaje de texto o por medio de una aplicación de mensajería (WhatsApp, etc.) ', '3.- Programé una cita vía mensaje de texto o por medio de una aplicación de mensajería (WhatsApp, etc.) '),
        ('4.- Recibí un recordatorio por parte del distribuidor', '4.- Recibí un recordatorio por parte del distribuidor'),
        ('5.- No hice una cita', '5.- No hice una cita'),
    ]   

    TIEMPO_ESPERA_ASESOR_CHOICES = [
        ('Inmediatamente', 'Inmediatamente'),
        ('de 1 a 2 minutos', 'de 1 a 2 minutos'),
        ('de 3 a 6 minutos', 'de 3 a 6 minutos'),
        ('Más de 6 minutos', 'Más de 6 minutos'),
        ('No lo sé', 'No lo sé'),
    ]

    ACCIONES_ASESOR_SELECTS = [
        ('Inspección completa de su vehiculo','Inspección completa de su vehiculo'),
        ('Enfoque totalmente en sus necesidades','Enfoque totalmente en sus necesidades'),
        ('Le indicó cuando estaría listo su vehiculo antes de empezar el servicio','Le indicó cuando estaría listo su vehiculo antes de empezar el servicio'),
        ('Te mantuvo informado del estado de tu vehículo','Te mantuvo informado del estado de tu vehículo'),
        ('Después de completar el servicio, revisó con usted el trabajo que se le ralizó a su vehiculo','Después de completar el servicio, revisó con usted el trabajo que se le ralizó a su vehiculo'),
    ]

    #fecha = forms.DateTimeField(disabled=True)
    fecha = forms.DateTimeField(widget=forms.HiddenInput(), required=False)

    numero_orden = forms.IntegerField()

    agencia = forms.Select()

    #1
    vivio_experiencia_completa = forms.TypedChoiceField(
        choices=[(True, 'Sí'), (False, 'No')],
        widget=forms.RadioSelect,
        coerce=lambda x: x == 'True',  # Asegura que se almacene como un booleano en el modelo
        label='¿Eres tú quien vivió toda la experiencia de servicio, desde la recepción hasta la entrega del vehículo?',
    )

    #2
    tipo_servicio = forms.ChoiceField(
        choices=TIPO_SERVICIO_VEHICULO,
        widget=forms.RadioSelect,
        label='¿Qué tipo de servicio se realizó a tu vehículo?'
    )

    recomendar_mitsubishi = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(11)],
        widget=forms.RadioSelect,
        label='En una escala de 0 a 10 puntos, ¿qué tan probable es que recomiendes a Mitsubishi San Angel a un amigo, familiar o colega?'
    )


    #4
    razones_recomendacion = forms.CharField(
        label='¿Cuáles son las razones por las que otorgas esta calificación?',
        widget=forms.Textarea(attrs={'class':'text_area'})

    )

    #5
    programacion_cita = forms.ChoiceField(
        choices=PROGRAMACION_CITA_SERVICIO_CHOICES,
         widget=forms.RadioSelect(attrs={'class': 'radio_select'}),
        label='¿Cómo programaste tu cita de servicio?'
    )

    calificacion_programacion_cita = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(11)],
        widget=forms.RadioSelect,
        label='Usando una escala de 0 a 10 puntos ¿cómo calificarías tu experiencia para programación de una cita?',
    )


    #7
    obtener_cita_deseada = forms.TypedChoiceField(
        choices=[(True, 'Sí'), (False, 'No')],
        widget=forms.RadioSelect,
        coerce=lambda x: x == 'True',  # Asegura que se almacene como un booleano en el modelo
        label='¿Te fue posible obtener una cita el día / horario deseado?',
    )

    #8
    calificacion_servicio_general = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(11)],
        widget=forms.RadioSelect,
        label='En una escala de 0 a 10 puntos, ¿qué tan probable es que recomiendes a Mitsubishi San Angel a un amigo, familiar o colega?'
    )

    #9
    tiempo_espera_asesor = forms.ChoiceField(
        choices=TIEMPO_ESPERA_ASESOR_CHOICES,
        widget=forms.RadioSelect,
        label='¿Cuál fue el tiempo de espera en la recepción de su vehículo?'
    )

    #10
    acciones_asesor = forms.MultipleChoiceField(
        label='Por favor indique las acciones realizadas por su asesor (puede seleccionar más de una opción)',
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices= ACCIONES_ASESOR_SELECTS,
    )

    #11
    calificacion_atencion_asesor = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(11)],
        widget=forms.RadioSelect,
        label='Usando una escala de 0 a 10 puntos ¿cómo calificarías en general la atención brindada por tu asesor?',
    )

    #12
    ofrecieron_cortesias = forms.TypedChoiceField(
        label='¿Te ofrecieron algún tipo de cortesías en el distribuidor (por ejemplo: agua, dulces, internet gratuito, etc.)?',
        choices=[(True, 'Sí'), (False, 'No')],
        widget=forms.RadioSelect,
        coerce=lambda x: x == 'True',  # Asegura que se almacene como un booleano en el modelo
    )
    
    #13
    calificacion_instalaciones = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(11)],
        widget=forms.RadioSelect,
        label='En una escala de 0 a 10 puntos, ¿qué tan probable es que recomiendes a Mitsubishi San Angel a un amigo, familiar o colega?'
    )

    #14
    vehiculo_entregado_prometido = forms.TypedChoiceField(
        label='¿Tu vehículo fue entregado en el día y a la hora prometidos?',
        choices=[(True, 'Sí'), (False, 'No')],
        widget=forms.RadioSelect,
        coerce=lambda x: x == 'True',  # Asegura que se almacene como un booleano en el modelo
    )

    #15
    costo_final_coincide_presupuesto = forms.ChoiceField(
        choices=COSTO_FINAL_CHOICES,
        widget=forms.RadioSelect,
        label='¿El costo final del servicio coincidió con el presupuesto inicial que te dieron?'
    )

    #16
    explicacion_reparaciones = forms.TypedChoiceField(
        label='¿Se te explicó las reparaciones hechas a tu vehiculo y las que quedaron pendientes?',
        choices=[(True, 'Sí'), (False, 'No')],
        widget=forms.RadioSelect,
        coerce=lambda x: x == 'True', 
    )

    #17
    limpieza_vehiculo = forms.TypedChoiceField(
        label='¿Recibiste tu automovil con la limpieza esperada?',
        choices=[(True, 'Sí'), (False, 'No')],
        widget=forms.RadioSelect,
        coerce=lambda x: x == 'True', 
    )

    #18
    calificacion_entrega_general = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(11)],
        widget=forms.RadioSelect,
        label='¿Cómo calificarías tu experiencia en general con el servicio brindado en su última visita por Mitsubishi San Angel?*'
    )
    
    def clean_acciones_asesor(self):
        selected_options = self.cleaned_data.get('acciones_asesor', [])
        return '. '.join(selected_options)
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        #instance.fecha = timezone.now()
        #instance.agencia_id = 1
        if commit:
            instance.save()
        return instance