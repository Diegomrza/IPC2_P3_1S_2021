from flask import Flask, request, jsonify, Response #Módulos de flask
from flask_cors import CORS #Politicas CORS
import re #Libreria de expresiones regulares
from xml.etree.ElementTree import XML, fromstring #Para parsear a xml
import xmltodict #archivo xml a diccionario
import xml.etree.ElementTree as ET #ElementTree

from Eventos import evento #Clase eventos
from Fechas import EventosPorFechas

#Listas
listaEventos = []
listaFechas = []
eventoxfecha = []

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return '<h1>El servidor está corriendo!</h1>'

@app.route('/ingreso', methods=['POST'])
def ingresar_datos():
    global listaEventos, listaFechas, eventoxfecha
    #Fecha, Correo, Codigo error,Usuarios afectados, Descripción
    datos = fromstring(request.data)

    for x in datos:
        #Fecha--------------------------------------------------------------------------
        busquedaFecha = re.compile(r'([3][01]|[012][0-9])\/([0][0-9]|[1][012])\/\d{4}')
        fecha = ''
        fecha = busquedaFecha.search(x.text)
        #Guardando todas las fechas ----------------------------------------------------
        bandera = True
        if len(listaFechas) != 0:
            for y in listaFechas:
                if y == fecha.group():
                    bandera = False
            if bandera:
                listaFechas.append(fecha.group())
        else:
            listaFechas.append(fecha.group())
        #Correo ------------------------------------------------------------------------
        busquedaCorreos = re.compile(r'[\w+.*]+\@[\w\.\w]+')
        correo = busquedaCorreos.search(x.text)
        #Codigo error ------------------------------------------------------------------
        busquedaError = re.compile(r'Error:\s*\d+')
        Error0 = busquedaError.search(x.text)
        Error1 = re.search(r'\d+', Error0.group())
        codigo_error = Error1.group()
        #Usuarios afectados ------------------------------------------------------------
        todos = busquedaCorreos.findall(x.text)
        Afectados = []
        for x in range(1, len(todos)):
            Afectados.append(todos[x])
        #Creación del usuario ----------------------------------------------------------
        nuevo = evento(correo.group(), fecha.group(), codigo_error)
        nuevo.usuarios_afectados = Afectados
        listaEventos.append(nuevo)

        #print('Fecha: ',fecha.group(),'\nCorreo: ', correo.group(), '\nError: ', codigo_error)
        #print('Usuarios Afectados: ', Afectados)
    
    
    for fecha in listaFechas:
        nuevaFecha = EventosPorFechas(fecha)
        usersAfectados = []
        for event in listaEventos:
            if fecha == event.fecha:
                nuevaFecha.eventos.append(event)
                nuevaFecha.cantidad_mensajes+=1
                for af in event.usuarios_afectados:
                    if len(usersAfectados) == 0:
                        usersAfectados.append(af)
                    elif af in usersAfectados:
                        continue
                    elif af not in usersAfectados:
                        usersAfectados.append(af)

        print('Fecha: - ',nuevaFecha.fecha,'Usuarios afectados corregido: \n', usersAfectados)
        nuevaFecha.usuarios_afectados = usersAfectados
        eventoxfecha.append(nuevaFecha)
    
    return '''<CONFIRMAR>Datos leídos correctamente</CONFIRMAR>'''

@app.route('/consulta')
def consultar_datos():
    global listaEventos, listaFechas, eventoxfecha

    xml = '<ESTADISTICAS>'

    for fecha in eventoxfecha:
        xml += '<ESTADISTICA>'#
        xml += '<FECHA>'+fecha.fecha+'</FECHA>'
        xml += '<CANTIDAD_MENSAJES>'+str(fecha.cantidad_mensajes)+'</CANTIDAD_MENSAJES>'
        xml += '<REPORTADO_POR>'#
        listaUsuarios = []
        for x in fecha.eventos:
            if len(listaUsuarios) == 0:
                listaUsuarios.append(x)
            elif x.correo in listaUsuarios:
                x.cantidad_mensajes_usuario += 1
                continue
            elif x.correo not in listaUsuarios:
                listaUsuarios.append(x)
                x.cantidad_mensajes_usuario += 1

        for z in listaUsuarios:
            xml += '<USUARIO>'
            xml += '<EMAIL>' + z.correo+ '</EMAIL>'
            xml += '<CANTIDAD_MENSAJES>'+str(z.cantidad_mensajes_usuario)+'</CANTIDAD_MENSAJES>'
            xml += '</USUARIO>'
        xml += '</REPORTADO_POR>'

        xml += '<AFECTADOS>'#
        for afectados in fecha.usuarios_afectados:
            xml += '<AFECTADO>'+afectados+'</AFECTADO>'
        xml += '</AFECTADOS>'
        
        xml += '</ESTADISTICA>'   
    xml += '</ESTADISTICAS>'

    return xml

@app.route('/FFU', methods=['POST'])
def filtrar_info_por_fecha_y_usuario():
    pass

@app.route('/FFC',methods=['POST'])
def filtrar_por_fecha_y_codigo_de_error():
    pass

if __name__ == '__main__':
    app.run(threaded = True,port = 4000, debug = True)