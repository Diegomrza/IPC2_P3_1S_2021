from django import forms

class prueba(forms.Form):
    textArea2 = forms.CharField(widget=forms.Textarea(), label='textArea2')
    textArea1 = forms.CharField(widget=forms.Textarea(), label='textArea1')
    ruta = forms.CharField(widget=forms.FileInput(), label='ruta')
    