# src/models/evolucion.py
class Evolucion:
    def __init__(self, id, nombre, requisito_nivel, mejoras):
        self.id = id
        self.nombre = nombre
        self.requisito_nivel = requisito_nivel
        self.mejoras = mejoras
        self.desbloqueada = False

    def verificar_desbloqueo(self, nivel_anterior):
        if not self.desbloqueada and nivel_anterior >= self.requisito_nivel:
            self.desbloqueada = True
            for mejora in self.mejoras.values():
                mejora.desbloqueada = True
            return True
        return False

    def nivel_total(self):
        return sum(mejora.nivel for mejora in self.mejoras.values())