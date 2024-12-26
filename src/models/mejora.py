# src/models/mejora.py
class Mejora:
    def __init__(self, id, nombre, costo_base, cantidad_base=1.0, multiplicador_costo=1.15):
        self.id = id
        self.nombre = nombre
        self.costo_base = costo_base
        self.cantidad_base = cantidad_base
        self.multiplicador_costo = multiplicador_costo
        self.nivel = 0  # Cantidad comprada
        self.desbloqueada = False
        self.cantidad = 0  # Cantidad generada por segundo
        self.cantidad_disponible = 0  # Nueva variable para la cantidad disponible

    def calcular_costo(self):
        return int(self.costo_base * (self.multiplicador_costo ** self.nivel))

    def obtener_generacion(self):
        return self.cantidad_base * self.nivel
    
    def actualizar_cantidad(self, cantidad_anterior, dt):
        self.cantidad_disponible += cantidad_anterior * dt
        self.cantidad = self.obtener_generacion()

    def obtener_descripcion(self):
        if not self.desbloqueada:
            return f"??? [Bloqueado]"
        return f'{self.nombre}\nNivel: {self.nivel}\nCosto: {self.calcular_costo()} datos'

    def puede_comprar(self, datos_actuales):
        return self.desbloqueada and datos_actuales >= self.calcular_costo()