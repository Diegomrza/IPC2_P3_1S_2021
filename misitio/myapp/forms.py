from django import forms

class prueba(forms.Form):
    dato = forms.CharField(widget=forms.Textarea(), label='textArea2')
    enviar = forms.CharField(widget=forms.Textarea(), label='textArea1')
    
    
