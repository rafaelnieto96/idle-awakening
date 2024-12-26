# src/config/settings.py
from kivy.config import Config

# Configuración de ventana
WINDOW_CONFIG = {
    'width': 400,
    'height': 700
}

# Configuración del juego
GAME_CONFIG = {
    'update_interval': 1.0,
    'transition_duration': 0.3
}

# Evoluciones y sus requisitos
EVOLUCIONES = {
    1: {
        'nombre': 'Binario a Lenguaje',
        'requisito_nivel': 0,
        'mejoras': {
            'procesador_bits': {'nombre': 'Procesador de Bits', 'costo_base': 10, 'incremento_dps': 1},
            'decodificador': {'nombre': 'Decodificador Básico', 'costo_base': 25, 'incremento_dps': 2},
            'patrones': {'nombre': 'Reconocedor de Patrones', 'costo_base': 100, 'incremento_dps': 5},
            'traductor': {'nombre': 'Traductor Binario-Texto', 'costo_base': 250, 'incremento_dps': 10},
            'silabas': {'nombre': 'Formador de Sílabas', 'costo_base': 1000, 'incremento_dps': 25},
            'palabras': {'nombre': 'Constructor de Palabras', 'costo_base': 2500, 'incremento_dps': 50},
            'vocabulario': {'nombre': 'Vocabulario Básico', 'costo_base': 10000, 'incremento_dps': 100},
            'asociador': {'nombre': 'Asociador Palabra-Significado', 'costo_base': 25000, 'incremento_dps': 250},
            'frases': {'nombre': 'Generador de Frases Simples', 'costo_base': 100000, 'incremento_dps': 1000},
            'comunicador': {'nombre': 'Comunicador Infantil', 'costo_base': 1000000, 'incremento_dps': 5000}
        }
    },
    # ... Aquí irían las otras evoluciones ...
}

# Configuración inicial de Kivy
def init_kivy():
    Config.set('input', 'mouse', 'mouse')
    Config.set('graphics', 'width', str(WINDOW_CONFIG['width']))
    Config.set('graphics', 'height', str(WINDOW_CONFIG['height']))