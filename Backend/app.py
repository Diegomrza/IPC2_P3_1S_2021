from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from flask_restful import Api
import re
from datos import Datos
from Errores import Errores

#Prueba
from xml.etree.ElementTree import XML, fromstring

import xmltodict
import xml.etree.ElementTree as ET

#Listas
lista_reportes = []
lista_errores = []
listaFechas = []

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return '<h1>El servidor está corriendo!</h1>'

@app.route('/ingresoDatos', methods=['POST'])
def ingresar_datos():
    global lista_reportes, lista_errores, listaFechas

    datos = fromstring(request.data)

    for x in datos:
        #Fecha
        busquedaFecha = re.compile(r'([3][01]|[012][0-9])\/([0][0-9]|[1][012])\/\d{4}')
        fecha = ''
        fecha = busquedaFecha.search(x.text)

        bandera = True

        if len(listaFechas) != 0:
            for y in listaFechas:
                if y == fecha.group():
                    bandera = False
            if bandera:
                listaFechas.append(fecha.group())
        else:
            listaFechas.append(fecha.group())

        #Correo usuario que reporta
        busquedaCorreos = re.compile(r'[\w+.*]+\@[\w\.\w]+')
        correoUsuarioQueReporta = busquedaCorreos.search(x.text)

        #creacion del usuario que reporta
        nuevoReporte = Datos(correoUsuarioQueReporta.group(), fecha.group())

        #Agregando el reporte a la lista de reportes
        lista_reportes.append(nuevoReporte)

        #Creando la lista de todos los correos encontrados
        listaTodosLosCorreos = busquedaCorreos.findall(x.text)

        #Lista con solo los usuarios afectados
        listaUsuariosAfectados = []

        #Agregando solo los correos de los usuarios afectados a dicha lista
        for x in range(1,len(listaTodosLosCorreos)):
            listaUsuariosAfectados.append(listaTodosLosCorreos[x])

        #Creacion del error nuevo
        nuevoError = Errores()
        nuevoError.fecha = fecha.group()
        nuevoError.id_usuario = correoUsuarioQueReporta.group()
        nuevoError.usuarios_afectados = listaUsuariosAfectados

        #Agregando el error a la lista de errores
        lista_errores.append(nuevoError)

    return '''<CONFIRMAR>
              Datos leídos correctamente
              </CONFIRMAR>'''

@app.route('/consultaDatos')
def consultar_datos():
    global lista_errores, lista_reportes, listaFechas
    xml = '<ESTADISTICAS>'

    print(listaFechas)
    print(lista_errores)
    print(lista_reportes)

    for fechas in listaFechas:
        xml += '<ESTADISTICA>'
        xml += '<FECHA>'+fechas+'</FECHA>'
        xml += '<CANTIDAD_MENSAJES>'+'</CANTIDAD_MENSAJES>'
        xml += '<REPORTADO_POR>'
        for x in lista_errores:
            if fechas == x.fecha:
                xml += '<USUARIO>'+x.id_usuario+'</USUARIO>'
        xml += '</REPORTADO_POR>'
        xml += '</ESTADISTICA>'   
                
    xml += '</ESTADISTICAS>'

    return xml

@app.route('/filtrarFechayUsuario')
def filtrar_info_por_fecha_y_usuario():
    pass

@app.route('/filtrarFechayCodigo')
def filtrar_por_fecha_y_codigo_de_error():
    pass

@app.route('/retornarXML',methods=['POST','GET'])
def retornarXML():

    x = 10
    y = 5

    string = fromstring(request.data)
    print('Prueba',type(string))

    #xmlnuevo = fromstring(string)
    xml2 = '<ESTADISTICAS>'
    for x in string:
        xml2 += '<ESTADISTICA>'
        xml2 += x.text
        xml2 += '</ESTADISTICA>'
    xml2 += '</ESTADISTICAS>'

    #xml = xmltodict(string)

    return ''

if __name__ == '__main__':
    app.run(threaded = True,port = 4000, debug = True)