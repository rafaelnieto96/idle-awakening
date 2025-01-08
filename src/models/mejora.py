class Mejora:
    def __init__(self, id, nombre, costo_base, cantidad_base=1.0):
        self.id = id
        self.nombre = nombre
        self.costo_base = costo_base
        self.cantidad_base = cantidad_base
        self.nivel = 0
        self.desbloqueada = False
        self.cantidad = 0
        self.cantidad_disponible = 0

    def calcular_costo(self):
        # Para mejoras de desbloqueo (4,8,12,16), el costo es fijo
        if self.id % 4 == 0:
            return self.costo_base
        # Para el resto, el costo aumenta con el nivel
        return self.costo_base * (1.15 ** self.nivel)

    def obtener_generacion(self):
        # Las mejoras de desbloqueo no generan nada
        if self.id % 4 == 0:
            return 0
        # Para el resto, la generación es nivel * cantidad_base
        return self.nivel * self.cantidad_base

    def puede_comprar(self, datos_disponibles):
        # Solo se puede comprar si está desbloqueada
        if not self.desbloqueada:
            return False
            
        # Para mejoras de desbloqueo, solo se pueden comprar una vez
        if self.id % 4 == 0 and self.nivel >= 1:
            return False
            
        return datos_disponibles >= self.calcular_costo()
    
    def actualizar_cantidad(self, cantidad_anterior, dt):
        self.cantidad_disponible += cantidad_anterior * dt
        self.cantidad = self.obtener_generacion()

    def obtener_descripcion(self):
        if not self.desbloqueada:
            return f"??? [Bloqueado]"
        return f'{self.nombre}\nNivel: {self.nivel}\nCosto: {self.calcular_costo()} datos'
