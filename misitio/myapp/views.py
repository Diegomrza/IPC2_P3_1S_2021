from django.shortcuts import render, HttpResponse
import requests
from .forms import prueba

endpoint = 'http://127.0.0.1:4000/'

# Create your views here.
def frontal(request):
    contexto = {
        'valor' : ''
    }
    return render(request, 'Frontal.html', contexto)
    
def enviar(request):
    contexto = {}
    form = prueba(request.GET)
    if form.is_valid():
        texto = form.cleaned_data['ruta']
        print(texto)
    response = requests.post(endpoint+'consulta')
    #contexto['ruta'] = texto
    valor = response.json()
    return render(request, 'Frontal.html', contexto)

def peticiones(request):
    return render(request, 'index.html')

def FFU(request):
    return render(request, 'FFU.html')

def FFC(request):
    return render(request, 'FFC.html')

def reset(request):
    response2 = requests.get(endpoint+'prueba2')
    return render(request, 'Frontal.html')