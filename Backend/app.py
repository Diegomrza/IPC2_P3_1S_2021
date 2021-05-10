from flask import Flask, request, jsonify, Response #Módulos de flask
from flask_cors import CORS #Politicas CORS
import re #Libreria de expresiones regulares
from xml.etree.ElementTree import XML, fromstring #Para parsear a xml
import xmltodict #archivo xml a diccionario
import xml.etree.ElementTree as ET #ElementTree


import matplotlib.pyplot as plt


from Eventos import evento #Clase eventos
from Fechas import EventosPorFechas
from usuarios import usuario, error

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origin":"*"}})

#Listas
listaEventos = []
listaFechas = []
eventoxfecha = []
#listaUsuarios = []

eventos = []
fechas = []
eventos_por_fecha = []

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


#Si el archivo xml viene con errores el método truena
@app.route('/ingreso', methods=['POST'])
def ingresar_datos():
    global listaEventos, listaFechas, eventoxfecha

    # C:\Users\Squery\Documents\GitHub\IPC2_Proyecto3_201901429\Backend\entrada1.xml

    if request.json != None:
        ruta = request.json['ruta']
        print(ruta)
        tree = ET.parse(r'C:\Users\Squery\Documents\GitHub\IPC2_Proyecto3_201901429\Backend\\'+ruta)
        datos = tree.getroot()
    else:
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

        #print('Fecha: - ',nuevaFecha.fecha,'Usuarios afectados corregido: \n', usersAfectados)
        nuevaFecha.usuarios_afectados = usersAfectados
        
        eventoxfecha.append(nuevaFecha)
    
    return jsonify({
        'valor':'Correcto'
    })


@app.route('/consultaFechas')
def consultaFechas():
    global listaFechas

    return jsonify({
        'valor': listaFechas
    })

@app.route('/consulta')
def consultar_datos():
    global listaEventos, listaFechas, eventoxfecha

    xml = '<ESTADISTICAS>\n'
    for fecha in eventoxfecha:
        xml += '\t<ESTADISTICA>\n'#
        xml += '\t\t<FECHA>'+fecha.fecha+'</FECHA>\n'
        xml += '\t\t<CANTIDAD_MENSAJES>'+str(fecha.cantidad_mensajes)+'</CANTIDAD_MENSAJES>\n'
        
        xml += '\t\t<REPORTADO_POR>\n'
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
            xml += '\t\t\t<USUARIO>\n'
            xml += '\t\t\t\t<EMAIL>' + listaUsuarios[z].correo+ '</EMAIL>\n'
            xml += '\t\t\t\t<CANTIDAD_MENSAJES>'+str(listaUsuarios[z].cantidad_mensajes_usuario)+'</CANTIDAD_MENSAJES>\n'
            xml += '\t\t\t</USUARIO>\n'
        
        xml += '\t\t</REPORTADO_POR>\n'
        xml += '\t\t<AFECTADOS>\n'#
        for afectados in fecha.usuarios_afectados:
            xml += '\t\t\t<AFECTADO>'+afectados+'</AFECTADO>\n'
        xml += '\t\t</AFECTADOS>\n'
        
        xml += '\t\t<ERRORES>\n'
        listaErrores = []
        for err in fecha.eventos:
            flag = False
            if len(listaErrores) == 0:
                objeto1 = error(err.codigo_error)
                listaErrores.append(objeto1)
            else:
                for i in range(0, len(listaErrores)):
                    if err.codigo_error == listaErrores[i].codigo_error:
                        listaErrores[i].cantidad_veces_error += 1
                        flag = True
                if flag == False:
                    objeto1 = error(err.codigo_error)
                    listaErrores.append(objeto1)
        for e in listaErrores:
            xml += '\t\t\t<ERROR>\n'
            xml += '\t\t\t\t<CODIGO>'+e.codigo_error+'</CODIGO>\n'
            xml += '\t\t\t\t<CANTIDAD_MENSAJES>'+str(e.cantidad_veces_error)+'</CANTIDAD_MENSAJES>\n'
            xml += '\t\t\t</ERROR>\n'
        xml += '\t\t</ERRORES>\n'
        
        xml += '\t</ESTADISTICA>\n'#   
    xml += '</ESTADISTICAS>'
    
    estadistica = open(r'C:\Users\Squery\Documents\GitHub\IPC2_Proyecto3_201901429\Backend\estadisticas.xml','w')
    estadistica.write(xml)
    estadistica.close()
    #return jsonify({'valor':xml})      
    #return xmltodict.parse(xml)
    #return xml
    return jsonify({
        'valor':xml
        })

@app.route('/FFU', methods=['POST'])
def filtrar_info_por_fecha_y_usuario():
    global listaEventos, listaFechas, eventoxfecha

    fechaP = request.json['opcion']
    print(fechaP)

    listaUsuarios = []
    for fecha in eventoxfecha:
        if fecha.fecha == fechaP:
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
    names = []
    values = []
    for f in listaUsuarios:
        names.append(f.correo)
        values.append(f.cantidad_mensajes_usuario)

    plt.figure(figsize=(9, 3))

    #plt.subplot(131)
    plt.bar(names, values)

    plt.suptitle('FFU')
    plt.savefig(r'C:\Users\Squery\Documents\GitHub\IPC2_Proyecto3_201901429\misitio\myapp\static\img\FFU.png')

    return jsonify({
        'message':'Excellent'
    })

@app.route('/FFC',methods=['POST'])
def filtrar_por_fecha_y_codigo_de_error():
    global listaEventos, listaFechas, eventoxfecha

    fechaC = '20/04/2021'

    listaErrores = []
    for fecha in eventoxfecha:
        if fecha.fecha == fechaC:
            for err in fecha.eventos:
                flag = False
                if len(listaErrores) == 0:
                    objeto1 = error(err.codigo_error)
                    listaErrores.append(objeto1)
                else:
                    for i in range(0, len(listaErrores)):
                        if err.codigo_error == listaErrores[i].codigo_error:
                            listaErrores[i].cantidad_veces_error += 1
                            flag = True
                    if flag == False:
                        objeto1 = error(err.codigo_error)
                        listaErrores.append(objeto1)
    
    names = []
    values = []
    for c in listaErrores:
        names.append(c.codigo_error)
        values.append(c.cantidad_veces_error)

    plt.figure(figsize=(9, 3))

    #plt.subplot(131)
    plt.bar(names, values)

    plt.suptitle('FFC')
    plt.savefig(r'C:\Users\Squery\Documents\GitHub\IPC2_Proyecto3_201901429\misitio\myapp\static\img\FFC.png')

    return jsonify({
        'message':'Excellent'
    })

@app.route('/reset')
def reset():
    global listaEventos, listaFechas, eventos_por_fecha, eventoxfecha, eventos, fechas

    listaEventos.clear()
    listaFechas.clear()
    eventos_por_fecha.clear()
    eventoxfecha.clear()
    eventos.clear()
    fechas.clear()

    print(listaEventos)
    print(listaFechas)
    print(eventos_por_fecha)
    print(eventoxfecha)
    print(eventos)
    print(fechas)

    return jsonify({
        'message':'Datos borrados'
    })

if __name__ == '__main__':
    app.run(threaded = True,port = 4000, debug = True)