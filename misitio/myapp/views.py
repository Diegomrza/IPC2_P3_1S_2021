from django.shortcuts import render, HttpResponse
import requests
from .forms import prueba

endpoint = 'http://127.0.0.1:4000/'

# Create your views here.
def index(request):
    contexto = {
        'valor' : ''
    }
    return render(request, 'Frontal.html', contexto)

def prueba(request):
    pass

def enviar(request):
    response = requests.post(endpoint+'ingreso')

    valor = response.json()
    contexto = {
        'valor' : valor
    }
    return render(request, 'Frontal.html', contexto)

def reset(request):
    response2 = requests.get(endpoint+'prueba2')

    return render(request, 'Frontal.html')