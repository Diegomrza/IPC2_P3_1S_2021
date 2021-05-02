from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from flask_restful import Api
import re

#Prueba
from xml.etree.ElementTree import XML, fromstring

import xmltodict
import xml.etree.ElementTree as ET

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return '<h1>El servidor está corriendo!</h1>'

@app.route('/consultaDatos')
def consultar_datos():
    pass

@app.route('/filtrarFyU')
def filtrar_info_por_fecha_y_usuario():
    pass

@app.route('/filtrarFyC')
def filtrar_por_fecha_y_codigo_de_error():
    pass

@app.route('/retornarXML',methods=['POST','GET'])
def retornarXML():

    x = 10
    y = 5
    
    string = request.data

    xml = '<ESTADISTICAS>\n'

    for e in range(0,x):
        xml+='<ESTADISTICA>'
        for t in range(0,y):
            xml+='hola\n'

        xml+='</ESTADISTICA>'

    xml += '</ESTADISTICAS>'

    #print(xml)

    xmlnuevo = fromstring(string)
    for x in xmlnuevo:
        print(x.tag)
        print(x.text)

    dicc = xmltodict.parse(xml)


    return xml

if __name__ == '__main__':
    app.run(threaded = True,port = 4000, debug = True)