from flask import Flask, request, jsonify, Response #Módulos de flask
from flask_cors import CORS #Politicas CORS
import re #Libreria de expresiones regulares
from xml.etree.ElementTree import XML, fromstring #Para parsear a xml
import xmltodict #archivo xml a diccionario
import xml.etree.ElementTree as ET #ElementTree

from Eventos import evento #Clase eventos
from Fechas import EventosPorFechas
from usuarios import usuario

#Listas
listaEventos = []
listaFechas = []
eventoxfecha = []
#listaUsuarios = []

#listas obsoletas
eventos = []
fechas = []
eventos_por_fecha = []


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return '<h1>El servidor está corriendo!</h1>'

#Obsoleto
@app.route('/ingresoDatos', methods=['POST'])
def lectura():
    global eventos, fechas, eventos_por_fecha
    datos = fromstring(request.data)
    for mensaje in datos:
        busquedaFecha = re.compile(r'([3][01]|[012][0-9])\/([0][0-9]|[1][012])\/\d{4}')
        busquedaCorreos = re.compile(r'[\w+.*]+\@[\w\.\w]+')
        busquedaError = re.compile(r'Error:\s*\d+')
        fecha = busquedaFecha.search(mensaje.text).group()
        bandera = True
        if len(fechas) != 0:
            for y in fechas:
                if y == fecha:
                    bandera = False
            if bandera:
                fechas.append(fecha)
        else:
            fechas.append(fecha)
        correo = busquedaCorreos.search(mensaje.text).group()
        error = re.search(r'\d+', busquedaError.search(mensaje.text).group()).group()
        todos_los_correos = busquedaCorreos.findall(mensaje.text)
        usuarios_afectados = []
        for a in range(1, len(todos_los_correos)):
            usuarios_afectados.append(todos_los_correos[a])
        nuevoEvento = evento(correo, fecha, error)
        nuevoEvento.usuarios_afectados = usuarios_afectados
        eventos.append(nuevoEvento)        

    #Eventos guardados por fecha
    for f in fechas:
        evento_por_fecha = EventosPorFechas(f)
        
        listaux = []
        for e in eventos:
            if e.fecha == f:
                evento_por_fecha.cantidad_mensajes+=1
                listaux.append(e)
        evento_por_fecha.eventos = listaux
        eventos_por_fecha.append(evento_por_fecha)

    return jsonify({'message':'Exito'})

#Fin Obsoleto

@app.route('/ingreso', methods=['POST'])
def ingresar_datos():
    global listaEventos, listaFechas, eventoxfecha
    #Fecha, Correo, Codigo error,Usuarios afectados, Descripción
    datos = fromstring(request.data)

    prueba = request.data.decode('utf-8')
    print(prueba)

    print(datos)

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

    xml = '<ESTADISTICAS>\n'
    for fecha in eventoxfecha:
        xml += '<ESTADISTICA>\n'#
        xml += '<FECHA>'+fecha.fecha+'</FECHA>\n'
        xml += '<CANTIDAD_MENSAJES>'+str(fecha.cantidad_mensajes)+'</CANTIDAD_MENSAJES>\n'
        xml += '<REPORTADO_POR>\n'#
        listaUsuarios = []
        for x in fecha.eventos:
            bandera = False
            if len(listaUsuarios) == 0:
                objeto = usuario(x.correo)
                listaUsuarios.append(objeto)
            else:
                
                for y in range(0, len(listaUsuarios)):
                    if x.correo == listaUsuarios[y].correo:
                        listaUsuarios[y].cantidad_mensajes_usuario+=1
                        bandera = True
                if bandera == False:
                    objeto = usuario(x.correo)
                    listaUsuarios.append(objeto)

        for z in range(0, len(listaUsuarios)):
            xml += '<USUARIO>\n'
            xml += '<EMAIL>' + listaUsuarios[z].correo+ '</EMAIL>\n'
            xml += '<CANTIDAD_MENSAJES>'+str(listaUsuarios[z].cantidad_mensajes_usuario)+'</CANTIDAD_MENSAJES>\n'
            xml += '</USUARIO>\n'
        xml += '</REPORTADO_POR>\n'

        xml += '<AFECTADOS>\n'#
        for afectados in fecha.usuarios_afectados:
            xml += '<AFECTADO>'+afectados+'</AFECTADO>\n'
        xml += '</AFECTADOS>\n'
        
        xml += '</ESTADISTICA>\n'   
    xml += '</ESTADISTICAS>'

    return jsonify({'valor':xml})
    #return xmltodict.parse(xml)
    #return xml

@app.route('/FFU', methods=['POST'])
def filtrar_info_por_fecha_y_usuario():
    pass

@app.route('/FFC',methods=['POST'])
def filtrar_por_fecha_y_codigo_de_error():
    pass

@app.route('/prueba', methods=['GET'])
def prueba():
    xml = '<ESTADISTICAS>\n'

    for x in range(0, 10):
        xml += '<ESTADISTICA>\n'
        for y in range(0, 5):
            xml += '\t<USUARIO>'+str(x)+'</USUARIO>\n'
        xml += '</ESTADISTICA>\n'
    xml += '</ESTADISTICAS>'
    print(xml)
    datos = {
        'valor': xml
    }
    return jsonify(datos)

@app.route('/prueba', methods=['POST'])
def prueba2():

    ruta = request.json['ruta']
    print(ruta)
    return jsonify({'message':'simon'})

if __name__ == '__main__':
    app.run(threaded = True,port = 4000, debug = True)