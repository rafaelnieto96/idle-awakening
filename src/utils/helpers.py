# src/utils/helpers.py
def format_number(n):
    """Formatea números grandes a formato legible"""
    if n < 1000:
        return str(int(n))
    if n < 1000000:
        return f"{n/1000:.1f}K"
    if n < 1000000000:
        return f"{n/1000000:.1f}M"
    return f"{n/1000000000:.1f}B"

def calcular_siguiente_costo(costo_base, nivel, multiplicador=1.15):
    """Calcula el costo de la siguiente mejora"""
    return int(costo_base * (multiplicador ** nivel))

def verificar_requisitos_evolucion(nivel_actual, mejoras_completadas):
    """Verifica si se cumplen los requisitos para la siguiente evolución"""
    requisitos = {
        2: 50,  # Nivel total de mejoras necesario para evolución 2
        3: 100, # Para evolución 3
        4: 200, # Para evolución 4
        5: 500  # Para evolución 5
    }
    return mejoras_completadas >= requisitos.get(nivel_actual + 1, float('inf'))