# src/models/mejora.py
class Mejora:
    def __init__(self, nombre, costo_base, incremento_dps, multiplicador_costo=1.15):
        self.nombre = nombre
        self.costo_base = costo_base
        self.incremento_dps = incremento_dps
        self.multiplicador_costo = multiplicador_costo
        self.nivel = 0
        self.desbloqueada = False

    def calcular_costo(self):
        return int(self.costo_base * (self.multiplicador_costo ** self.nivel))

    def obtener_descripcion(self):
        if not self.desbloqueada:
            return f"??? [Bloqueado]"
        return f'{self.nombre}\nNivel: {self.nivel}\nCosto: {self.calcular_costo()} datos'

    def puede_comprar(self, datos_actuales):
        return self.desbloqueada and datos_actuales >= self.calcular_costo()