class usuario:
    def __init__(self, correo):
        self.correo = correo
        self.cantidad_mensajes_usuario = 1

class error:
    def __init__(self, codigo_error):
        self.codigo_error = codigo_error
        self.cantidad_veces_error = 1