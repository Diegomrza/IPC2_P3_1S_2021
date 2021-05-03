class Errores:
    def __init__(self):
        self.codigo_error = None
        self.usuarios_afectados = []
        self.fecha = None
        self.id_usuario = None #Aquí va el correo del usuario y funcionará como id
        self.cantidad_de_mensajes = 0
    
    def devolver_error(self, id):
        pass