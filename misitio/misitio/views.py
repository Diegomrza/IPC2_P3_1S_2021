from django.http import HttpResponse
import datetime

def home(request):

    return HttpResponse('Servidor en linea!')

def saludo(request):

    return HttpResponse('Hola mucho gusto')

def despedida(request):

    return HttpResponse('Hasta la próxima')

def fecha_actual(request):

    fecha_actual = datetime.datetime.now()

    fecha = '''<html>
    <body>
    <h1>
    Fecha y hora actuales: %s
    </h1>
    </body>
    </html>''' %fecha_actual

    return HttpResponse(fecha)