import datetime
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand
from ..models import Encuesta
import pandas as pd

class Command(BaseCommand):
    help = 'Envía un archivo Excel con los datos de las encuestas del día anterior'

    def handle(self, *args, **kwargs):
        # Obtener la fecha de ayer
        fecha_ayer = datetime.date.today() - datetime.timedelta(days=1)

        # Filtrar las encuestas llenadas el día anterior
        encuestas_ayer = Encuesta.objects.filter(fecha__date=fecha_ayer)

        # Crear un DataFrame de pandas con los datos de las encuestas
        data = []
        for encuesta in encuestas_ayer:
            data.append({
                'Fecha': encuesta.fecha,
                'Numero de Orden': encuesta.numero_orden,
                # Agrega más campos aquí según sea necesario
            })
        df = pd.DataFrame(data)

        # Guardar el DataFrame como un archivo Excel
        nombre_archivo = f'encuestas_{fecha_ayer}.xlsx'
        df.to_excel(nombre_archivo, index=False)

        # Enviar el archivo Excel por correo electrónico
        asunto = 'Encuestas del día: ' + + fecha_ayer
        cuerpo = 'Adjunto encontrarás el archivo Excel con las encuestas del día anterior de la empresa Mitsubishi Morelos.'
        destinatario = 'soporte@amsamex.comx.mx'
        email = EmailMessage(asunto, cuerpo, to=[destinatario])
        email.attach_file(nombre_archivo)
        email.send()

        self.stdout.write(self.style.SUCCESS('El archivo Excel se ha enviado correctamente por correo electrónico.'))
