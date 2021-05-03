class evento:
    #Fecha, correo,codigo error, usuarios afectados
    def __init__(self, correo, fecha, codigo_error):
        self.correo = correo
        self.fecha = fecha
        self.codigo_error = codigo_error
        self.usuarios_afectados = []
        self.cantidad_mensajes_usuario = 0