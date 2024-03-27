from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from ..sx_surveys.models import Agencias, Encuesta
import pandas as pd
import json
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
import csv

'''
@login_required
def dashboard_view_v2(request):
    # Obtén la lista de agencias para mostrar en el template
    agencias = Agencias.objects.all()

    # Inicializar variables
    fecha_inicio = None
    fecha_fin = None
    fecha_actual = None
    total_surveys = 0
    encuestas = None
    df = None

    # Procesar el formulario
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        fecha_actual = 'Fecha actual'
        if fecha_inicio == fecha_fin:
            datetime_p = timezone.localtime(timezone.now())
            encuestas = Encuesta.objects.filter(fecha__contains=fecha_inicio)
            total_surveys = Encuesta.objects.filter(fecha__contains=fecha_inicio).count()
            if encuestas.exists():
                df = pd.DataFrame(list(encuestas.values()))
        else: 
            encuestas_a = Encuesta.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
            encuestas_b = Encuesta.objects.filter(fecha__contains=fecha_fin)
            #encuestas = Encuesta.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
            encuestas = encuestas_a.union(encuestas_b)
            total_surveys = encuestas_a.union(encuestas_b).count()
            if encuestas.exists(): 
                print(list(encuestas.values()))
                df = pd.DataFrame(list(encuestas.values()))
    else:
        # Cargar la página con la fecha actual por defecto
        fecha_actual = timezone.now().strftime('%Y-%m-%d')
        fecha_inicio = 'Fecha_inicio'
        fecha_fin = 'Fecha_fin'
        encuestas = Encuesta.objects.filter(fecha__contains=fecha_actual)
        total_surveys = Encuesta.objects.filter(fecha__contains=fecha_actual).count()
        if encuestas.exists():  # Verificar si hay encuestas encontradas
            # Convertir datos a un DataFrame de Pandas
            df = pd.DataFrame(list(encuestas.values()))

    # Verifica la existencia de las columnas
    if df is not None:
        fig1 = px.pie(df, names='recomendar_mitsubishi', title='Recomiendan mitsubishi San Angel')
        fig2 = px.pie(df, names='tipo_servicio', title='Distribución de Tipos de Servicio')
        fig3 = px.pie(df, names='calificacion_servicio_general', title='Calificación del Servicio General')
        fig1.update_layout(template="plotly_dark")
        fig2.update_layout(template="plotly_dark")
        fig3.update_layout(template="plotly_dark")

        # Convertir figuras a HTML
        fig1_html = fig1.to_html(full_html=False)
        fig2_html = fig2.to_html(full_html=False)
        fig3_html = fig3.to_html(full_html=False)

        # Renderizar el template con las gráficas y los datos
        return render(request, 'sx_dashboard/dashboard.html', {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'agencias': agencias,
            'fecha_actual': fecha_actual,
            'fig1': fig1_html,
            'fig2': fig2_html,
            'fig3': fig3_html,
            'total_surveys': total_surveys
        })
    else:
        # No se encontraron encuestas, enviar un mensaje al template
        return render(request, 'sx_dashboard/dashboard.html', {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'agencias': agencias,
            'fecha_actual': fecha_actual,
            'total_surveys': total_surveys,
            'message': 'No se encontraron formularios en las fechas seleccionadas.'
        })

'''



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

        # Recorrer las encuestas y agrupar los números de orden por calificación, servicios, etc.
        for encuesta in encuestas:
            calificacion = encuesta.calificacion_servicio_general
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

        # Convertir los datos a formato JSON
        data_json = json.dumps(data)
        data_json_services = json.dumps(data_services)
        data_json_recomendar_mitsu = json.dumps(data_recomendar_mitsu)
        data_json_calificacion_servicio_general = json.dumps(data_calificacion_servicio_general)

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

        # Recorrer las encuestas y agrupar los números de orden por calificación, servicios, etc.
        for encuesta in encuestas:
            calificacion = encuesta.calificacion_servicio_general
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

        # Convertir los datos a formato JSON
        data_json = json.dumps(data)
        data_json_services = json.dumps(data_services)
        data_json_recomendar_mitsu = json.dumps(data_recomendar_mitsu)
        data_json_calificacion_servicio_general = json.dumps(data_calificacion_servicio_general)

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
        })
    
    else:
        # No se encontraron encuestas, enviar un mensaje al template
        return render(request, 'sx_dashboard/dashboard_asam.html', {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'agencias': agencias
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
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="datos_encuestas{fecha_inicio}.csv"'

            # Crear el escritor CSV
            writer = csv.writer(response)

            # Escribir las filas de encuestas en el archivo CSV
            writer.writerow(['Orden', 'Fecha', 'Vivio experiencia completa'])  # Encabezados
            for encuesta in encuestas_filtradas:
                writer.writerow([encuesta.numero_orden, encuesta.fecha, encuesta.vivio_experiencia_completa])  # Datos de cada encuesta

            print('Se tiene que descargar el acrhivo')
            return response
        else:
            print("Por favor, proporcione fechas de inicio y fin.")
            return HttpResponse("Por favor, proporcione fechas de inicio y fin.")
    else:
        print("Esta vista solo admite solicitudes POST o no has mandado  fechas.")
        return HttpResponse("Esta vista solo admite solicitudes POST.")

@login_required
def dashboard_chartjs(request):
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

@login_required
def get_survey_modal_dos(request):
    if request.method == 'POST' and 'numero_orden' in request.POST:
        numero_orden = request.POST.get('numero_orden')
        try:
            encuesta = Encuesta.objects.get(numero_orden=numero_orden)
            # Aquí puedes ajustar los campos que deseas devolver en la respuesta JSON

            data_encuesta = {
                'Número de orden: ': encuesta.numero_orden,
                'Fecha de la encuesta: ' : encuesta.fecha,
                'El cliente vivió toda la experiencia de servicio, desde la recepción hasta la entrega del vehículo?: ': encuesta.vivio_experiencia_completa,
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