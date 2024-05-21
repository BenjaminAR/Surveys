from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from ..sx_surveys.models import Agencias, Encuesta, Encuesta_automotores
import json
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import smart_str
import csv
from io import BytesIO
from reportlab.pdfgen import canvas

#descargar_excel
from django.views.decorators.csrf import csrf_exempt
import openpyxl
from datetime import datetime


def default_fecha():
    fecha_actual = timezone.now() - timezone.timedelta(hours=6)
    return fecha_actual.strftime('%Y-%m-%d')

@login_required
def dashboard_view(request):
    agencias = Agencias.objects.all()
    fecha_inicio = None
    fecha_fin = None
    fecha_actual = None
    total_surveys = 0
    encuestas = None
    df = None

    if request.method == 'POST':
        # Manejar el formulario de selección de fechas
        if 'fecha_inicio' in request.POST and 'fecha_fin' in request.POST:
            fecha_inicio = request.POST.get('fecha_inicio')
            fecha_fin = request.POST.get('fecha_fin')
            fecha_actual = 'Fecha actual'

            # Filtrar encuestas por rango de fechas
            if fecha_inicio == fecha_fin:
                encuestas = Encuesta.objects.filter(fecha__contains=fecha_inicio, agencia_id=1)
            else: 
                encuestas_a = Encuesta.objects.filter(fecha__range=[fecha_inicio, fecha_fin], agencia_id=1)
                encuestas_b = Encuesta.objects.filter(fecha__contains=fecha_fin, agencia_id=1)
                encuestas = encuestas_a.union(encuestas_b)

            total_surveys = encuestas.count()

        # Manejar la solicitud de consulta por número de orden
        elif 'numero_orden' in request.POST:
            numero_orden = request.POST.get('numero_orden')
            try:
                encuesta = Encuesta.objects.get(numero_orden=numero_orden)
                return render(request, 'sx_surveys/get_order.html', {'encuesta': encuesta})
            except Encuesta.DoesNotExist:
                mensaje_error = "No se encontró ninguna encuesta con el número de orden proporcionado."
                return render(request, 'sx_surveys/get_order.html', {'mensaje_error': mensaje_error})

    else:
        #fecha_actual = timezone.now().strftime('%Y-%m-%d')
        fecha_actual = default_fecha()
        fecha_inicio = fecha_actual
        fecha_fin = fecha_actual
        encuestas = Encuesta.objects.filter(fecha__contains=fecha_actual, agencia_id=1)
        total_surveys = encuestas.count()

    # Inicializar diccionarios para almacenar los números de orden por calificación, servicios, etc.
    if encuestas is not None:
        data = {}
        data_services = {}
        data_recomendar_mitsu = {}
        data_calificacion_servicio_general = {}
        data_calificacion_entrega_general = {}
        data_calificacion_atencion_asesor = {}
        data_calificacion_instalaciones= {}

        # Recorrer las encuestas y agrupar los números de orden por calificación, servicios, etc.
        for encuesta in encuestas:
            calificacion = encuesta.calificacion_programacion_cita
            numero_orden = encuesta.numero_orden
            if calificacion not in data:
                data[calificacion] = [numero_orden]
            else:
                data[calificacion].append(numero_orden)
            
            servicios = encuesta.tipo_servicio
            if servicios not in data_services:
                data_services[servicios] = [numero_orden]
            else:
                data_services[servicios].append(numero_orden)

            recomendar_mitsu = encuesta.recomendar_mitsubishi
            if recomendar_mitsu not in data_recomendar_mitsu:
                data_recomendar_mitsu[recomendar_mitsu] = [numero_orden]
            else:
                data_recomendar_mitsu[recomendar_mitsu].append(numero_orden)

            calificacion_servicio_general_ = encuesta.calificacion_servicio_general
            if calificacion_servicio_general_ not in data_calificacion_servicio_general:
                data_calificacion_servicio_general[calificacion_servicio_general_] = [numero_orden]
            else:
                data_calificacion_servicio_general[calificacion_servicio_general_].append(numero_orden)
            
            calificacion_entrega_general_ = encuesta.calificacion_entrega_general
            if calificacion_entrega_general_ not in data_calificacion_entrega_general:
                data_calificacion_entrega_general[calificacion_entrega_general_] = [numero_orden]
            else:
                data_calificacion_entrega_general[calificacion_entrega_general_].append(numero_orden)
            
            calificacion_atencion_asesor_ = encuesta.calificacion_atencion_asesor
            if calificacion_atencion_asesor_ not in data_calificacion_atencion_asesor:
                data_calificacion_atencion_asesor[calificacion_atencion_asesor_] = [numero_orden]
            else:
                data_calificacion_atencion_asesor[calificacion_atencion_asesor_].append(numero_orden)
            
            calificacion_instalaciones_ = encuesta.calificacion_instalaciones
            if calificacion_instalaciones_ not in data_calificacion_instalaciones:
                data_calificacion_instalaciones[calificacion_instalaciones_] = [numero_orden]
            else:
                data_calificacion_instalaciones[calificacion_instalaciones_].append(numero_orden)

        # Convertir los datos a formato JSON
        data_json = json.dumps(data)
        data_json_services = json.dumps(data_services)
        data_json_recomendar_mitsu = json.dumps(data_recomendar_mitsu)
        data_json_calificacion_servicio_general = json.dumps(data_calificacion_servicio_general)
        data_json_calificacion_entrega_general = json.dumps(data_calificacion_entrega_general)
        data_json_calificacion_atencion_asesor = json.dumps(data_calificacion_atencion_asesor)
        data_json_calificacion_instalaciones = json.dumps(data_calificacion_instalaciones)

        # Renderizar la plantilla con los datos necesarios
        return render(request, 'sx_dashboard/dashboard.html', {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'agencias': agencias,
            'fecha_actual': fecha_actual,
            'total_surveys': total_surveys,
            'data_json': data_json,
            'data_json_services': data_json_services,
            'data_json_recomendar_mitsu': data_json_recomendar_mitsu,
            'data_json_calificacion_servicio_general': data_json_calificacion_servicio_general,
            'data_json_calificacion_entrega_general': data_json_calificacion_entrega_general,
            'data_json_calificacion_atencion_asesor': data_json_calificacion_atencion_asesor,
            'data_json_calificacion_instalaciones' : data_json_calificacion_instalaciones,
        })
    
    else:
        msj = f'No se han encotrado encuastas en {fecha_actual}'
        # No se encontraron encuestas, enviar un mensaje al template
        return render(request, 'sx_dashboard/dashboard.html', {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'agencias': agencias,
            'msj' : msj,
        })

@login_required
def dashboard_view_asam(request):
    agencias = Agencias.objects.all()
    fecha_inicio = None
    fecha_fin = None
    fecha_actual = None
    total_surveys = 0
    encuestas = None
    df = None

    if request.method == 'POST':
        # Manejar el formulario de selección de fechas
        if 'fecha_inicio' in request.POST and 'fecha_fin' in request.POST:
            fecha_inicio = request.POST.get('fecha_inicio')
            fecha_fin = request.POST.get('fecha_fin')
            fecha_actual = 'Fecha actual'

            # Filtrar encuestas por rango de fechas
            if fecha_inicio == fecha_fin:
                encuestas = Encuesta.objects.filter(fecha__contains=fecha_inicio, agencia_id=2)
            else: 
                encuestas_a = Encuesta.objects.filter(fecha__range=[fecha_inicio, fecha_fin], agencia_id=2)
                encuestas_b = Encuesta.objects.filter(fecha__contains=fecha_fin, agencia_id=2)
                encuestas = encuestas_a.union(encuestas_b)

            total_surveys = encuestas.count()

        # Manejar la solicitud de consulta por número de orden
        elif 'numero_orden' in request.POST:
            numero_orden = request.POST.get('numero_orden')
            try:
                encuesta = Encuesta.objects.get(numero_orden=numero_orden)
                return render(request, 'sx_surveys/get_order.html', {'encuesta': encuesta})
            except Encuesta.DoesNotExist:
                mensaje_error = "No se encontró ninguna encuesta con el número de orden proporcionado."
                return render(request, 'sx_surveys/get_order.html', {'mensaje_error': mensaje_error})

    else:
        #fecha_actual = timezone.now().strftime('%Y-%m-%d')
        fecha_actual = default_fecha()
        fecha_inicio = fecha_actual
        fecha_fin = fecha_actual
        encuestas = Encuesta.objects.filter(fecha__contains=fecha_actual, agencia_id=2)
        total_surveys = encuestas.count()

    # Inicializar diccionarios para almacenar los números de orden por calificación, servicios, etc.
    if encuestas is not None:
        data = {}
        data_services = {}
        data_recomendar_mitsu = {}
        data_calificacion_servicio_general = {}
        data_calificacion_entrega_general = {}
        data_calificacion_atencion_asesor = {}
        data_calificacion_instalaciones= {}

        # Recorrer las encuestas y agrupar los números de orden por calificación, servicios, etc.
        for encuesta in encuestas:
            calificacion = encuesta.calificacion_programacion_cita
            numero_orden = encuesta.numero_orden
            if calificacion not in data:
                data[calificacion] = [numero_orden]
            else:
                data[calificacion].append(numero_orden)
            
            servicios = encuesta.tipo_servicio
            if servicios not in data_services:
                data_services[servicios] = [numero_orden]
            else:
                data_services[servicios].append(numero_orden)

            recomendar_mitsu = encuesta.recomendar_mitsubishi
            if recomendar_mitsu not in data_recomendar_mitsu:
                data_recomendar_mitsu[recomendar_mitsu] = [numero_orden]
            else:
                data_recomendar_mitsu[recomendar_mitsu].append(numero_orden)

            calificacion_servicio_general_ = encuesta.calificacion_servicio_general
            if calificacion_servicio_general_ not in data_calificacion_servicio_general:
                data_calificacion_servicio_general[calificacion_servicio_general_] = [numero_orden]
            else:
                data_calificacion_servicio_general[calificacion_servicio_general_].append(numero_orden)
            
            calificacion_entrega_general_ = encuesta.calificacion_entrega_general
            if calificacion_entrega_general_ not in data_calificacion_entrega_general:
                data_calificacion_entrega_general[calificacion_entrega_general_] = [numero_orden]
            else:
                data_calificacion_entrega_general[calificacion_entrega_general_].append(numero_orden)
            
            calificacion_atencion_asesor_ = encuesta.calificacion_atencion_asesor
            if calificacion_atencion_asesor_ not in data_calificacion_atencion_asesor:
                data_calificacion_atencion_asesor[calificacion_atencion_asesor_] = [numero_orden]
            else:
                data_calificacion_atencion_asesor[calificacion_atencion_asesor_].append(numero_orden)
            
            calificacion_instalaciones_ = encuesta.calificacion_instalaciones
            if calificacion_instalaciones_ not in data_calificacion_instalaciones:
                data_calificacion_instalaciones[calificacion_instalaciones_] = [numero_orden]
            else:
                data_calificacion_instalaciones[calificacion_instalaciones_].append(numero_orden)

        # Convertir los datos a formato JSON
        data_json = json.dumps(data)
        data_json_services = json.dumps(data_services)
        data_json_recomendar_mitsu = json.dumps(data_recomendar_mitsu)
        data_json_calificacion_servicio_general = json.dumps(data_calificacion_servicio_general)
        data_json_calificacion_entrega_general = json.dumps(data_calificacion_entrega_general)
        data_json_calificacion_atencion_asesor = json.dumps(data_calificacion_atencion_asesor)
        data_json_calificacion_instalaciones = json.dumps(data_calificacion_instalaciones)

        # Renderizar la plantilla con los datos necesarios
        return render(request, 'sx_dashboard/dashboard_asam.html', {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'agencias': agencias,
            'fecha_actual': fecha_actual,
            'total_surveys': total_surveys,
            'data_json': data_json,
            'data_json_services': data_json_services,
            'data_json_recomendar_mitsu': data_json_recomendar_mitsu,
            'data_json_calificacion_servicio_general': data_json_calificacion_servicio_general,
            'data_json_calificacion_entrega_general': data_json_calificacion_entrega_general,
            'data_json_calificacion_atencion_asesor': data_json_calificacion_atencion_asesor,
            'data_json_calificacion_instalaciones' : data_json_calificacion_instalaciones,
        })
    
    else:
        # No se encontraron encuestas, enviar un mensaje al template
        return render(request, 'sx_dashboard/dashboard_asam.html', {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'agencias': agencias
        })
    
@login_required
def dashboard_view_amsa(request):
    fecha_inicio = None
    fecha_fin = None
    fecha_actual = None
    total_surveys = 0
    encuestas = None
    df = None

    if request.method == 'POST':
        # Manejar el formulario de selección de fechas
        if 'fecha_inicio' in request.POST and 'fecha_fin' in request.POST:
            fecha_inicio = request.POST.get('fecha_inicio')
            fecha_fin = request.POST.get('fecha_fin')
            fecha_actual = 'Fecha actual'

            # Filtrar encuestas por rango de fechas
            if fecha_inicio == fecha_fin:
                encuestas = Encuesta_automotores.objects.filter(fecha__contains=fecha_inicio, agencia_id=3)
            else: 
                encuestas_a = Encuesta_automotores.objects.filter(fecha__range=[fecha_inicio, fecha_fin], agencia_id=3)
                encuestas_b = Encuesta_automotores.objects.filter(fecha__contains=fecha_fin, agencia_id=3)
                encuestas = encuestas_a.union(encuestas_b)

            total_surveys = encuestas.count()

        # Manejar la solicitud de consulta por número de orden
        elif 'numero_orden' in request.POST:
            numero_orden = request.POST.get('numero_orden')
            try:
                encuesta = Encuesta_automotores.objects.get(numero_orden=numero_orden)
                return render(request, 'sx_surveys/get_order.html', {'encuesta': encuesta})
            except Encuesta_automotores.DoesNotExist:
                mensaje_error = "No se encontró ninguna encuesta con el número de orden proporcionado."
                return render(request, 'sx_surveys/get_order.html', {'mensaje_error': mensaje_error})

    else:
        #fecha_actual = timezone.now().strftime('%Y-%m-%d')
        fecha_actual = default_fecha()
        fecha_inicio = fecha_actual
        fecha_fin = fecha_actual
        encuestas = Encuesta_automotores.objects.filter(fecha__contains=fecha_actual, agencia_id=3)
        total_surveys = encuestas.count()

    # Inicializar diccionarios para almacenar los números de orden por calificación, servicios, etc.
    if encuestas is not None:
        data = {}  #calificacion
        data_services = {}
        data_recomendar = {}
        data_calificacion_instalaciones_amenidades = {}
        data_capacidad_asesor_generar_confianza = {}
        data_calificacion_asesor_general = {}
        

        # Recorrer las encuestas y agrupar los números de orden por calificación, servicios, etc.
        for encuesta in encuestas:
            calificacion = encuesta.programacion_cita
            numero_orden = encuesta.numero_orden
            if calificacion not in data:
                data[calificacion] = [numero_orden]
            else:
                data[calificacion].append(numero_orden)
            
            servicios = encuesta.tipo_trabajo_realizado
            if servicios not in data_services:
                data_services[servicios] = [numero_orden]
            else:
                data_services[servicios].append(numero_orden)

            recomendar = encuesta.recomendar_a_familiares_amigos
            if recomendar not in data_recomendar:
                data_recomendar[recomendar] = [numero_orden]
            else:
                data_recomendar[recomendar].append(numero_orden)

            #Actulizar data_recomendar_mitsu a data_recomentar en front

            calificacion_instalaciones_amenidades_ = encuesta.calificacion_instalaciones_amenidades
            if calificacion_instalaciones_amenidades_ not in data_calificacion_instalaciones_amenidades:
                data_calificacion_instalaciones_amenidades[calificacion_instalaciones_amenidades_] = [numero_orden]
            else:
                data_calificacion_instalaciones_amenidades[calificacion_instalaciones_amenidades_].append(numero_orden)
            

            calificacion_atencion_asesor_ = encuesta.capacidad_asesor_generar_confianza
            if calificacion_atencion_asesor_ not in data_capacidad_asesor_generar_confianza:
                data_capacidad_asesor_generar_confianza[calificacion_atencion_asesor_] = [numero_orden]
            else:
                data_capacidad_asesor_generar_confianza[calificacion_atencion_asesor_].append(numero_orden)


            calificacion_asesor_general_ = encuesta.calificacion_asesor_general
            if calificacion_asesor_general_ not in data_calificacion_asesor_general:
                data_calificacion_asesor_general[calificacion_asesor_general_] = [numero_orden]
            else:
                data_calificacion_asesor_general[calificacion_asesor_general_].append(numero_orden)
        

        # Convertir los datos a formato JSON
        data_json = json.dumps(data)
        data_json_services = json.dumps(data_services)
        data_json_recomendar = json.dumps(data_recomendar)
        data_json_calificacion_instalaciones_amenidades = json.dumps(data_calificacion_instalaciones_amenidades)
        data_json_calificacion_atencion_asesor = json.dumps(data_capacidad_asesor_generar_confianza)
        data_json_data_calificacion_asesor_general = json.dumps(data_calificacion_asesor_general)


        # Renderizar la plantilla con los datos necesarios
        return render(request, 'sx_dashboard/dashboard_amsa.html', {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'fecha_actual': fecha_actual,
            'total_surveys': total_surveys,
            'data_json': data_json,
            'data_json_services': data_json_services,
            'data_json_recomendar': data_json_recomendar,
            'data_json_calificacion_instalaciones_amenidades': data_json_calificacion_instalaciones_amenidades,
            'data_json_calificacion_atencion_asesor': data_json_calificacion_atencion_asesor,
            'data_json_data_calificacion_asesor_general': data_json_data_calificacion_asesor_general,
        })
    
    else:
        # No se encontraron encuestas, enviar un mensaje al template
        return render(request, 'sx_dashboard/dashboard_amsa.html', {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
        })    

@login_required
def download_filtered_data(request):
    if request.method == 'POST':
        if 'fecha_inicio' in request.POST and 'fecha_fin' in request.POST:
            fecha_inicio = request.POST.get('fecha_inicio')
            fecha_fin = request.POST.get('fecha_fin')
            sucursal_id = request.POST.get('sucursal')
            fecha_actual = 'Fecha actual'
            print('\n\n\n' + fecha_inicio + '\n' + fecha_fin + '\n\n\n')
            # Filtrar encuestas por rango de fechas
            if fecha_inicio == fecha_fin:
                encuestas_filtradas = Encuesta.objects.filter(fecha__contains=fecha_inicio, agencia_id=sucursal_id)
                print('Fechas Iguales')
            else: 
                encuestas_a = Encuesta.objects.filter(fecha__range=[fecha_inicio, fecha_fin], agencia_id=sucursal_id)
                encuestas_b = Encuesta.objects.filter(fecha__contains=fecha_fin, agencia_id=sucursal_id)
                encuestas_filtradas = encuestas_a.union(encuestas_b)
                

            # Crear el objeto de respuesta HTTP
            response = HttpResponse(content_type='text/csv; charset=utf-8' )
            response['Content-Disposition'] = f'attachment; filename="datos_encuestas{fecha_inicio}.csv"'

            # Crear el escritor CSV
            writer = csv.writer(response)

            # Escribir las filas de encuestas en el archivo CSV
            writer.writerow(['Orden', 
                             'Fecha y hora', 
                             'Vivio experiencia completa',
                             'Tipo de servicio',
                             'Del 0 al 10 recomiendan a la agencia',
                             'Razones por las que recomiendan',
                             #Servicio
                             'Vehículo entregado en tiempo pometido',
                             '¿El costo final coincide con el presupuesto?',
                             'Explicación sobre las reparaciones',
                             '¿El vehículo se entrego limpio?',
                             'Del 0 al 10 calificación general de la entrega',
                              #Asesor
                              'Tiempo de espera del asesor para la entrega',
                              'Acciones realizadas por el asesor',
                              'Del 0 al 10 calificación al asesor',
                              #Insalaciones
                              'Ofrecieron cortesias durante la estadía?',
                              'Del 0 al 10 Calificación a las instalaciones',
                              #Entrega
                              'Como programo la cita',
                              'Del 0 al 10 calificación al programar una cita',
                              'Agendó cita el dia/horario deseado',
                              #Calificación general
                              'Del 0 al 10 calificaión general del servicio',
                              ])
                        
            for encuesta in encuestas_filtradas:
                writer.writerow([encuesta.numero_orden, 
                                 encuesta.fecha, 
                                 encuesta.vivio_experiencia_completa_texto(),
                                 encuesta.tipo_servicio,
                                 encuesta.recomendar_mitsubishi,
                                 encuesta.razones_recomendacion,
                                 #Servicio
                                 encuesta.vehiculo_entregado_prometido_texto(),
                                 encuesta.costo_final_coincide_presupuesto,
                                 encuesta.explicacion_reparaciones_texto(),
                                 encuesta.limpieza_vehiculo_texto(),
                                 encuesta.calificacion_entrega_general,
                                 #Asesor
                                 encuesta.tiempo_espera_asesor,
                                 encuesta.acciones_asesor,
                                 encuesta.calificacion_atencion_asesor,
                                 #Instalaciones
                                 encuesta.ofrecieron_cortesias,
                                 encuesta.calificacion_instalaciones,
                                 #Entrega
                                 smart_str(encuesta.programacion_cita),
                                 encuesta.calificacion_programacion_cita,
                                 encuesta.obtener_cita_deseada,

                                 encuesta.calificacion_servicio_general,
                                 
                                 ])
                

            print('Se tiene que descargar el acrhivo')
            return response
        else:
            print("Por favor, proporcione fechas de inicio y fin.")
            return HttpResponse("Por favor, proporcione fechas de inicio y fin.")
    else:
        print("Esta vista solo admite solicitudes POST o no has mandado  fechas.")
        return HttpResponse("Esta vista solo admite solicitudes POST.")


    agencias = Agencias.objects.all()
    fecha_inicio = None
    fecha_fin = None
    fecha_actual = None
    total_surveys = 0
    encuestas = None
    df = None

    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        fecha_actual = 'Fecha actual'
        if fecha_inicio == fecha_fin:
            datetime_p = timezone.localtime(timezone.now())
            encuestas = Encuesta.objects.filter(fecha__contains=fecha_inicio)
            total_surveys = Encuesta.objects.filter(fecha__contains=fecha_inicio).count()

        else: 
            encuestas_a = Encuesta.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
            encuestas_b = Encuesta.objects.filter(fecha__contains=fecha_fin)
            encuestas = encuestas_a.union(encuestas_b)
            total_surveys = encuestas_a.union(encuestas_b).count()

    else:
        # Cargar la página con la fecha actual por defecto
        fecha_actual = timezone.now().strftime('%Y-%m-%d')
        fecha_inicio = 'Fecha_inicio'
        fecha_fin = 'Fecha_fin'
        encuestas = Encuesta.objects.filter(fecha__contains=fecha_actual)
        total_surveys = Encuesta.objects.filter(fecha__contains=fecha_actual).count()


    # Inicializa un diccionario para almacenar los números de orden por calificación
    if encuestas is not None:

        data = {}
        data_services = {}
        data_recomendar_mitsu = {}
        data_calificacion_servicio_general = {}

        # Recorre las encuestas y agrupa los números de orden por calificación
        for encuesta in encuestas:
            calificacion = encuesta.calificacion_servicio_general
            numero_orden = encuesta.numero_orden
            if calificacion not in data:
                data[calificacion] = [numero_orden]
            else:
                data[calificacion].append(numero_orden)
        
        for x in encuestas:
            servicios = x.tipo_servicio
            numero_orden = x.numero_orden
            if servicios not in data_services:
                data_services[servicios] = [numero_orden]
            else:
                data_services[servicios].append(numero_orden)

        
        for y in encuestas:
            recomendar_mitsu = y.recomendar_mitsubishi
            numero_orden = y.numero_orden

            if recomendar_mitsu not in data_recomendar_mitsu:
                data_recomendar_mitsu[recomendar_mitsu] = [numero_orden]

            else:
                data_recomendar_mitsu[recomendar_mitsu].append(numero_orden)

        for i in encuestas:
            calificacion_servicio_general_ = i.calificacion_servicio_general
            numero_orden = i.numero_orden

            if calificacion_servicio_general_ not in data_calificacion_servicio_general:
                data_calificacion_servicio_general[calificacion_servicio_general_] = [numero_orden]

            else:
                data_calificacion_servicio_general[calificacion_servicio_general_].append(numero_orden)



        # Convierte los datos a formato JSON
        data_json = json.dumps(data)
        data_json_services = json.dumps(data_services)
        data_json_recomendar_mitsu = json.dumps(data_recomendar_mitsu)
        data_json_calificacion_servicio_general = json.dumps(data_calificacion_servicio_general)


        # Renderiza la plantilla con los datos necesarios
        return render(request, 'sx_dashboard/dashboard_chartjs.html', {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'agencias': agencias,
            'fecha_actual': fecha_actual,
            'total_surveys': total_surveys,
            'data_json': data_json,
            'data_json_services': data_json_services,
            'data_json_recomendar_mitsu': data_json_recomendar_mitsu,
            'data_json_calificacion_servicio_general': data_json_calificacion_servicio_general,
            })
    
    else:
        # No se encontraron encuestas, enviar un mensaje al template
        return render(request, 'sx_dashboard/dashboard_chartjs.html', {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'agencias': agencias,
            'fecha_actual': fecha_actual,
            'total_surveys': total_surveys,
            'message': 'No se encontraron formularios en las fechas seleccionadas.'
        })

@login_required
def dashboard_pruebas(request):
    pass

@login_required
def get_survey_modal(request):
    if request.method == 'POST' and 'numero_orden' in request.POST:
        numero_orden = request.POST.get('numero_orden')
        print("Número de orden recibido en la vista:", numero_orden)
        try:
            encuesta = Encuesta.objects.get(numero_orden=numero_orden)
            # Generar el contenido HTML del modal
            modal_content = render_to_string('sx_dashboard/survey_modal.html', {'encuesta': encuesta})
            return JsonResponse({'modal_content': modal_content})
        except Encuesta.DoesNotExist:
            return JsonResponse({'error': 'No se encontró ninguna encuesta con el número de orden proporcionado.'}, status=404)
    else:
        return JsonResponse({'error': 'Se requiere un número de orden válido.'}, status=400)

    if request.method == 'POST' and 'numero_orden' in request.POST:
        numero_orden = request.POST.get('numero_orden')
        try:
            encuesta = Encuesta.objects.get(numero_orden=numero_orden)
            # Aquí puedes ajustar los campos que deseas devolver en la respuesta JSON

            data_encuesta = {
                'Número de orden: ': encuesta.numero_orden,
                'Fecha de la encuesta: ' : encuesta.fecha,
                'El cliente vivió toda la experiencia de servicio, desde la recepción hasta la entrega del vehículo?: ': encuesta.vivio_experiencia_completa_texto(),
                'El tipo de servicio que se realizo a su vehículo: ': encuesta.tipo_servicio,
                'De 0 a 10 recomendo a la agencia: ': encuesta.recomendar_mitsubishi,
                'Razon(es) por las que ha decidido calificar su recomendación: ': encuesta.razones_recomendacion,
                'El vehículo le fue entregado el día y hroa prometidos: ':encuesta.programacion_cita,
                'De 0 a 10 recomendo a la agencia: ':encuesta.calificacion_programacion_cita
            }

            return JsonResponse(data_encuesta)
        except Encuesta.DoesNotExist:
            return JsonResponse({'error': 'No se encontró ninguna encuesta con el número de orden proporcionado.'}, status=404)
    else:
        return JsonResponse({'error': 'Se requiere un número de orden válido.'}, status=400)

@login_required
def download_filtered_data_pdf(request):
    if request.method == 'POST' and 'numero_orden' in request.POST:
        numero_orden = request.POST.get('numero_orden')
        
        try:
            encuesta = Encuesta.objects.get(numero_orden=numero_orden)
            # Generar el contenido del PDF
            response = JsonResponse({'success': True})
            response['Content-Disposition'] = f'attachment; filename="encuesta_{encuesta.numero_orden}.pdf"'
            # Crea el PDF aquí con la información de la encuesta
            buffer = BytesIO()
            pdf = canvas.Canvas(buffer)
            pdf.setFont("Helvetica", 11)
            y_position = 790
            pdf.drawString(60, y_position, f'Agencia: {encuesta.agencia}')
            y_position -= 25
            pdf.drawString(60, y_position, f'Número de orden: {encuesta.numero_orden}')
            y_position -= 25
            pdf.drawString(60, y_position, f'Fecha: {encuesta.fecha_texto()}')
            y_position -= 25
            pdf.drawString(60, y_position, f'¿El cliente vivió la experiencia completa?: {encuesta.vivio_experiencia_completa_texto()}')
            y_position -= 25
            pdf.drawString(60, y_position, f'Tipo de servicio: {encuesta.tipo_servicio}')
            y_position -= 20
            pdf.drawString(60, y_position, f'¿Recomienda a la agencia?: {encuesta.recomendar_mitsubishi}')
            y_position -= 25
            pdf.drawString(60, y_position, f'Razones por las que recomiendan: {encuesta.razones_recomendacion}')
            y_position -= 20
            pdf.drawString(60, y_position, f'¿El vehículo fue entregado en el tiempo pometido?: {encuesta.vehiculo_entregado_prometido_texto()}')
            y_position -= 25
            pdf.drawString(60, y_position, f'¿El costo final coincidio con el presupuesto?: {encuesta.costo_final_coincide_presupuesto}')
            y_position -= 20
            pdf.drawString(60, y_position, f'¿Se le explicarion las reparaciones realizadas?: {encuesta.explicacion_reparaciones_texto()}')
            y_position -= 25
            pdf.drawString(60, y_position, f'¿El vehículo se entrego limpio?: {encuesta.limpieza_vehiculo_texto()}')
            y_position -= 20
            pdf.drawString(60, y_position, f'Del 0 al 10 calificación general de la entrega: {encuesta.calificacion_entrega_general}')
            #Asesor
            y_position -= 25
            pdf.drawString(60, y_position, f'Tiempo de espera del asesor para la entrega: {encuesta.tiempo_espera_asesor}')
            y_position -= 25
            pdf.drawString(60, y_position, f'Acciones realizadas por el asesor: {encuesta.acciones_asesor_con_saltos_de_linea()}')
            y_position -= 25
            pdf.drawString(60, y_position, f'Del 0 al 10 calificación al asesor: {encuesta.calificacion_atencion_asesor}')
            #Instalaciones
            y_position -= 25
            pdf.drawString(60, y_position, f'¿Se ofrecieron cortesias durante las estadía?: {encuesta.ofrecieron_cortesias_texto()}')
            y_position -= 25
            pdf.drawString(60, y_position, f'Del 0 al 10 Calificación a las instalaciones: {encuesta.calificacion_instalaciones}')       
            #Entrega
            y_position -= 25
            pdf.drawString(60, y_position, f'¿Como se programo la cita?: ')
            y_position -= 15
            pdf.drawString(70, y_position, f'{encuesta.programacion_cita}')
            y_position -= 25
            pdf.drawString(60, y_position, f'Del 0 al 10 calificación al programar una cita: {encuesta.calificacion_programacion_cita}')
            y_position -= 25
            pdf.drawString(60, y_position, f'¿Agendó cita el dia/horario deseado?: {encuesta.obtener_cita_deseada_texto()}')
            
            y_position -= 60
            pdf.drawString(190, y_position, f'Del 0 al 10 calificaión general del servicio: {encuesta.calificacion_servicio_general}')

            pdf.showPage()
            pdf.save()
            pdf_content = buffer.getvalue()
            buffer.close()
            response.content = pdf_content
            return response
        except Encuesta.DoesNotExist:
            return JsonResponse({'error': 'No se encontró ninguna encuesta con el número de orden proporcionado.'}, status=404)
    else:
        return JsonResponse({'error': 'Se requiere un número de orden válido.'}, status=400)

@login_required
def get_survey_modal_amsa(request):

    if request.method == 'POST' and 'numero_orden' in request.POST:
        numero_orden = request.POST.get('numero_orden')
        print("Número de orden recibido en la vista:", numero_orden)
        try:
            encuesta = Encuesta_automotores.objects.get(numero_orden=numero_orden)
            # Generar el contenido HTML del modal
            modal_content = render_to_string('sx_dashboard/survey_modal_amsa.html', {'encuesta': encuesta})
            return JsonResponse({'modal_content': modal_content})
        except encuesta.DoesNotExist:
            return JsonResponse({'error': 'No se encontró ninguna encuesta con el número de orden proporcionado.'}, status=404)
    else:
        return JsonResponse({'error': 'Se requiere un número de orden válido.'}, status=400)

@login_required
def download_filtered_data_pdf_amsa(request):
    if request.method == 'POST' and 'numero_orden' in request.POST:
        numero_orden = request.POST.get('numero_orden')
        
        try:
            encuesta = Encuesta_automotores.objects.get(numero_orden=numero_orden)
            # Generar el contenido del PDF
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="encuesta_{encuesta.numero_orden}.pdf"'
            
            buffer = BytesIO()
            pdf = canvas.Canvas(buffer)
            pdf.setFont("Helvetica", 10)

            # Establecer márgenes
            margin_left = 60
            margin_top = 790
            line_height = 15
            y_position = margin_top

            def draw_text(pdf, text):
                lines = pdf.beginText(margin_left, y_position)
                lines.textLines(text)
                pdf.drawText(lines)
                return lines.getY()

            y_position = draw_text(pdf, f'Agencia:{encuesta.agencia}')
            y_position -= line_height
            y_position = draw_text(pdf, f'Número de orden: {encuesta.numero_orden}')
            y_position -= line_height
            y_position = draw_text(pdf, f'Fecha: {encuesta.fecha_formateada()}')
            y_position -= line_height
            y_position = draw_text(pdf, f'Nombre del cliente: {encuesta.nombre_cliente}')
            y_position -= line_height
            y_position = draw_text(pdf, f'Número de telefono: {encuesta.numero_telefono}')
            y_position -= line_height
            y_position = draw_text(pdf, f'Correo: {encuesta.correo_cliente}')
            y_position -= line_height
            y_position = draw_text(pdf, f'Del 0 al 10 que tan probable es que recomiende a amigo y familiares: {encuesta.recomendar_a_familiares_amigos}')
            y_position -= line_height
            y_position = draw_text(pdf, f'Tipo de trabajo: {encuesta.tipo_trabajo_realizado}')
            y_position -= line_height
            y_position = draw_text(pdf, f'Del 0 al 10 proceso para agendar cita: {encuesta.programacion_cita}')
            y_position -= line_height
            y_position = draw_text(pdf, f'¿Cita en en dia y hoario deseado?: {encuesta.sacar_cita_deseada_texto()}')
            y_position -= line_height
            y_position = draw_text(pdf, f'¿Cómo programó esta visita de servicio?: {encuesta.como_programo_visita_servicio}')
            y_position -= line_height
            y_position = draw_text(pdf, f'¿Trasporte alternativo?: {encuesta.apoyo_transporte_alternativo}')
            y_position -= line_height
            y_position = draw_text(pdf, f'Del 0 al 10 calificación a instalaciones: {encuesta.calificacion_instalaciones_amenidades}')
            y_position -= line_height
            y_position = draw_text(pdf, f'Del 0 al 10 calificación al asesor al atender necesidades: {encuesta.capacidad_asesor_entender_necesidades}')
            y_position -= line_height
            y_position = draw_text(pdf, f'Del 0 al 10 calificación al asesor en general: {encuesta.calificacion_asesor_general}')
            y_position -= line_height
            y_position = draw_text(pdf, f'¿Se mantuvo informado del estado del vehículo?: {encuesta.mantener_informado_estado_vehiculo_texto()}')
            y_position -= line_height
            y_position = draw_text(pdf, f'Del 0 al 10 calificación a las explicaciones del asesor: {encuesta.detalle_explicaciones_asesor}')
            y_position -= line_height
            y_position = draw_text(pdf, f'Del 0 al 10 calificación al asesor al generar confianza: {encuesta.capacidad_asesor_generar_confianza}')
            y_position -= line_height
            y_position = draw_text(pdf, f'¿El trabajo fue completado a la primera?: {encuesta.trabajo_completado_primera_texto()}')
            y_position -= line_height
            y_position = draw_text(pdf, f'Motivos: {encuesta.motivo_trabajo_no_completado_primera_texto()}')
            y_position -= line_height
            y_position = draw_text(pdf, f'Del 0 al 10 calificación a las condiciones del vehículo en la enterga: {encuesta.condiciones_vehiculo_despues_trabajo}')
            y_position -= line_height
            y_position = draw_text(pdf, f'Del 0 al 10 calificación a la limpieza del vehículo en la entrega: {encuesta.limpieza_vehiculo_devolucion}')
            y_position -= line_height
            y_position = draw_text(pdf, f'¿Se le contacto con una llamada despues del servicio al vehículo?: {encuesta.llamada_cortesia_despues_entrega_vehiculo_texto()}')
            y_position -= line_height
            y_position = draw_text(pdf, f'¿El vehículo fue entregado a la hora acordada?: {encuesta.vehiculo_listo_hora_acordada_texto()}')
            y_position -= line_height
            y_position = draw_text(pdf, f'¿Consideró que el personal del distribuidor valoró su tiempo, durante su visita al taller?: {encuesta.personal_distribuidor_valoro_tiempo_texto()}')
            
            pdf.showPage()
            pdf.save()
            pdf_content = buffer.getvalue()
            buffer.close()
            response.content = pdf_content
            return response
        except Encuesta_automotores.DoesNotExist:
            return JsonResponse({'error': f'No se encontró ninguna encuesta con el número de orden proporcionado. {numero_orden}'}, status=404)
    else:
        return JsonResponse({'error': 'Se requiere un número de orden válido.'}, status=400)

    
@csrf_exempt
def descargar_excel_amsa(request):
    if request.method == 'POST':
        print('Se accedio a la funcion descargar_excel_amsa')
        fecha_inicio = request.POST.get('fechaInicio')
        fecha_fin = request.POST.get('fechaFin')

        # Convertir las fechas a objetos datetime
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').replace(tzinfo=None)
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').replace(tzinfo=None)

        # Filtrar las encuestas por rango de fechas
        encuestas = Encuesta_automotores.objects.filter(fecha__range=[fecha_inicio, fecha_fin])

        # Crear un archivo Excel
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Encuestas"

        # Escribir encabezados
        headers = ["Número de orden", "Fecha", "Nombre del cliente", "Teléfono",
                   "Correo", "Recomienda a familiares y amigos", "Tipo de tarbajo realizado",
                   "Programacion de cita", "¿Saco cita en fecha y hora?", "¿Como programo visita a servicio?",
                   "¿Tipo de trasporte alternativo?", "Calificación a las instalaciones y amenidades", "Calificación al asesor atender nececidades",
                   "Calificación al asesor en general", "¿Se mantuvo informado del estado del vehículo?", "Calificación al detalle de las explicaciones del asesor", 
                   "Calificacion para generar confianza del asesor", "¿El tarbajo se completo a la primera?", "Razones de no haberse completado a la primera",
                   "Calificación al vehículo despues de la entrega", "Calificación a la limpieza del vehículo a la devolución", "¿Se realizo una llamada de cortesia?",
                   "¿Vehículo entregado a tiempo?", "¿El personal valoro tiempo?"]
        ws.append(headers)

        # Escribir datos
        for encuesta in encuestas:
            row = [encuesta.numero_orden,  encuesta.fecha_formateada(), encuesta.nombre_cliente, encuesta.numero_telefono,
                   encuesta.correo_cliente, encuesta.recomendar_a_familiares_amigos, encuesta.tipo_trabajo_realizado, 
                   encuesta.programacion_cita, encuesta.sacar_cita_deseada_texto(), encuesta.como_programo_visita_servicio,
                   encuesta.apoyo_transporte_alternativo, encuesta.calificacion_instalaciones_amenidades, encuesta.capacidad_asesor_entender_necesidades,
                   encuesta.calificacion_asesor_general, encuesta.mantener_informado_estado_vehiculo_texto(), encuesta.detalle_explicaciones_asesor,
                   encuesta.capacidad_asesor_generar_confianza, encuesta.trabajo_completado_primera_texto(), encuesta.motivo_trabajo_no_completado_primera_texto(),
                   encuesta.condiciones_vehiculo_despues_trabajo, encuesta.limpieza_vehiculo_devolucion, encuesta.llamada_cortesia_despues_entrega_vehiculo_texto(),
                   encuesta.vehiculo_listo_hora_acordada_texto(), encuesta.personal_distribuidor_valoro_tiempo_texto()]
            ws.append(row)

        # Preparar la respuesta HTTP
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=encuestas.xlsx'

        # Guardar el archivo en la respuesta
        wb.save(response)

        return response

    return HttpResponse("Método no permitido", status=405)    