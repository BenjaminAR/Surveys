# forms.py
from django import forms
from .models import Encuesta, Encuesta_automotores
from .widgets import *

class EncuestaFormMitsu(forms.ModelForm):

    class Meta:
        model = Encuesta
        fields = '__all__'

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

    nombre_cliente = forms.CharField(required=True)
    numero_telefono = forms.CharField(required=True)
    correo_cliente = forms.EmailField(required=True)

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
    
    def clean_numero_telefono(self):
        numero_telefono = self.cleaned_data.get('numero_telefono')
        if not numero_telefono.replace('+', '').replace(' ', '').isdigit():
            raise forms.ValidationError("El número de teléfono debe contener solo números, espacios o un signo de más (+).")
        return numero_telefono.replace(' ', '')  # Eliminar espacios en blanco
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        #instance.fecha = timezone.now()
        #instance.agencia_id = 1
        self.full_clean()  # Realizar todas las validaciones
        if commit:
            instance.save()
        return instance


class EncuestaFormAmsa(forms.ModelForm):

    class Meta:
        model = Encuesta_automotores
        fields = '__all__'

    TIPO_TRABAJO_VEHICULO_CHOICES = [
        ('Mantenimiento Programado: Póliza de mantenimiento. ', 'Mantenimiento Programado: Póliza de mantenimiento. '),
        ('Reparaciones de Garantía: Falla reportada por el cliente cubierta por la garantía.','Reparaciones de Garantía: Falla reportada por el cliente cubierta por la garantía.'),
        ('Mantenimiento Correctivo: Reemplazo de partes de desgaste y reparación de fallas fuera de garantía.', 'Mantenimiento Correctivo: Reemplazo de partes de desgaste y reparación de fallas fuera de garantía.'),
        ('Campaña: Llamado a revisión de acuerdo con los comunicados emitidos por la marca.', 'Campaña: Llamado a revisión de acuerdo con los comunicados emitidos por la marca.'),
        ('Otro','Otro'),
    ]
    
    PROGRAMACION_CITA_SERVICIO_CHOICES = [
        ('Llamó para pedir una cita.', 'Llamó para pedir una cita.'),
        ('Por un medio digital (página web, aplicación móvil, WhatsApp)', 'Por un medio digital (página web, aplicación móvil, WhatsApp)'),
        ('El distribuidor le llamó para ofrecerle la cita.', 'El distribuidor le llamó para ofrecerle la cita.'),
    ]

    TRASPORTE_ALTERNATIVO = [
        ('Uber', 'Uber'),
        ('Didi', 'Didi'),
        ('Taxi','Taxi'),
        ('Otro','Otro'),

    ]

    MOTIVO_TRABAJO_NO_COMPLETO_CHOICES = [
        ('El distribuidor no pudo encontrar el problema y/o no se presentó.', 'El distribuidor no pudo encontrar el problema y/o no se presentó.'),
        ('El vehículo volvió a averiarse tras ser reparado (misma falla).', 'El vehículo volvió a averiarse tras ser reparado (misma falla).'),
        ('Las piezas y/o refacciones para reparar el vehículo no estaban disponibles.', 'Las piezas y/o refacciones para reparar el vehículo no estaban disponibles.'),
        ('El trabajo realizado no corrigió el problema inicial.', 'El trabajo realizado no corrigió el problema inicial.'),
        ('El distribuidor provocó un nuevo problema que no existía anteriormente.', 'El distribuidor provocó un nuevo problema que no existía anteriormente.'),
        ('Falta de capacitación por parte de los técnicos.', 'Falta de capacitación por parte de los técnicos.'),
        ('El distribuidor me informó que el vehículo está funcionando según lo diseñado.', 'El distribuidor me informó que el vehículo está funcionando según lo diseñado.'),
        ('Decidí no completar las reparaciones.', 'Decidí no completar las reparaciones.'),
        ('El distribuidor se olvidó de completar la reparación o algo no se completó como se esperaba.', 'El distribuidor se olvidó de completar la reparación o algo no se completó como se esperaba.'),
    ]   

    #Datos de control
    fecha = forms.DateTimeField(widget=forms.HiddenInput(), required=False)
    numero_orden = forms.IntegerField()
    agencia = forms.Select()
    #Datos personales cliente
    nombre_cliente = forms.CharField(required=True)
    numero_telefono = forms.CharField(required=True)
    correo_cliente = forms.EmailField(required=True)


    #1
    recomendar_a_familiares_amigos = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(11)],
        widget=forms.RadioSelect,
        label='En una escala de 0 a 10 puntos, ¿qué tan probable es que recomiendes a Mitsubishi San Angel a un amigo, familiar o colega?'
    )

    #2
    tipo_trabajo_realizado = forms.ChoiceField(
        choices=TIPO_TRABAJO_VEHICULO_CHOICES,
        widget=forms.RadioSelect,
        label='¿Qué tipo de trabajo le fue realizado a su vehículo?'
    )

    
    #3
    programacion_cita = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(11)],
        widget=forms.RadioSelect,
        label='En una escala de 0 a 10 puntos, ¿Cómo califica el proceso para programar su cita al taller de servicio?'
    )

    #4
    sacar_cita_deseada = forms.TypedChoiceField(
        choices=[(True, 'Sí'), (False, 'No')],
        widget=forms.RadioSelect,
        coerce=lambda x: x == 'True',
        label='¿Pudo sacar una cita el día/hora que usted quiso?',
    )

    #5
    como_programo_visita_servicio = forms.ChoiceField(
        choices=PROGRAMACION_CITA_SERVICIO_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'radio_select'}),
        label='¿Cómo programó esta visita de servicio?'
    )
    
    #6
    apoyo_transporte_alternativo = forms.ChoiceField(
        choices=TRASPORTE_ALTERNATIVO,
        widget=forms.RadioSelect(attrs={'class': 'radio_select'}),
        label='¿Se le ofreció apoyo para solicitar transporte alternativo?, seleccione cuál.'
    )
    
    #7
    calificacion_instalaciones_amenidades = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(11)],
        widget=forms.RadioSelect,
        label='En una escala de 0 a 10 puntos, ¿Cómo evalúa las instalaciones del distribuidor y las amenidades ofrecidas?'
    )
    
    #8
    capacidad_asesor_entender_necesidades = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(11)],
        widget=forms.RadioSelect,
        label='En una escala de 0 a 10 puntos, ¿Cómo califica la capacidad del asesor para entender sus necesidades y responder a sus preguntas?'
    )
    
    #9
    calificacion_asesor_general = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(11)],
        widget=forms.RadioSelect,
        label='En una escala de 0 a 10 puntos, ¿Cómo evalúa a su asesor de servicio en general?'
    )
    
    #10
    mantener_informado_estado_vehiculo = forms.TypedChoiceField(
        label='¿El asesor de servicio le mantuvo informado del estado de su vehículo durante su visita al taller?',
        choices=[(True, 'Sí'), (False, 'No')],
        widget=forms.RadioSelect,
        coerce=lambda x: x == 'True',  
    )
    
    #11
    detalle_explicaciones_asesor = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(11)],
        widget=forms.RadioSelect,
        label='Usando una escala de 0 a 10 puntos, ¿Cómo califica el detalle de las explicaciones que su asesor de servicio le brindó?',
    )
    
    #12
    capacidad_asesor_generar_confianza = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(11)],
        widget=forms.RadioSelect,
        label='En una escala de 0 a 10 puntos, ¿Cómo califica la capacidad del asesor para generar confianza con respecto al servicio prestado?'
    )
    
    #13
    trabajo_completado_primera = forms.TypedChoiceField(
        label='¿El trabajo fue completado bien y a la primera?',
        choices=[(True, 'Sí'), (False, 'No')],
        widget=forms.RadioSelect,
        coerce=lambda x: x == 'True',
    )
    
    #14
    motivo_trabajo_no_completado_primera = forms.ChoiceField(
        choices=MOTIVO_TRABAJO_NO_COMPLETO_CHOICES,
        widget=forms.RadioSelect,
        label='¿Por qué considera que los trabajos solicitados no fueron realizados bien y a la primera?',
        required=False
    )

    #15
    condiciones_vehiculo_despues_trabajo = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(11)],
        widget=forms.RadioSelect,
        label='En una escala de 0 a 10 puntos, ¿Cómo califica las condiciones del vehículo después del trabajo realizado, con respecto al estado original?'
    )

    #16
    limpieza_vehiculo_devolucion = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(11)],
        widget=forms.RadioSelect,
        label='En una escala de 0 a 10 puntos, ¿Cómo califica la limpieza del vehículo en la devolución?'
    )

    #17
    llamada_cortesia_despues_entrega_vehiculo = forms.TypedChoiceField(
        label='¿Recibió una llamada de cortesía de su distribuidor unos días después de la entrega de su vehículo?',
        choices=[(True, 'Sí'), (False, 'No')],
        widget=forms.RadioSelect,
        coerce=lambda x: x == 'True', 
    )

    #18
    vehiculo_listo_hora_acordada = forms.TypedChoiceField(
        label='¿El vehículo estuvo listo a la hora acordada?',
        choices=[(True, 'Sí'), (False, 'No')],
        widget=forms.RadioSelect,
        coerce=lambda x: x == 'True', 
    )

    personal_distribuidor_valoro_tiempo = forms.TypedChoiceField(
        label='¿Considera que el personal del distribuidor valoró su tiempo, durante su visita al taller?',
        choices=[(True, 'Sí'), (False, 'No')],
        widget=forms.RadioSelect,
        coerce=lambda x: x == 'True', 
    )
    
    def clean_acciones_asesor(self):
        selected_options = self.cleaned_data.get('acciones_asesor', [])
        return '. '.join(selected_options)
    
    def clean_numero_telefono(self):
        numero_telefono = self.cleaned_data.get('numero_telefono')
        if not numero_telefono.replace('+', '').replace(' ', '').isdigit():
            raise forms.ValidationError("El número de teléfono debe contener solo números, espacios o un signo de más (+).")
        return numero_telefono.replace(' ', '')  # Eliminar espacios en blanco
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        #instance.fecha = timezone.now()
        #instance.agencia_id = 1
        self.full_clean()  # Realizar todas las validaciones
        if commit:
            instance.save()
        return instance