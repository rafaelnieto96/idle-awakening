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
    'transition_duration': 0.3,
    'currency': {
        'initial_amount': 1110,  # Cantidad inicial de datos
        'click_amount': 1,    # Cantidad que se obtiene por click (si implementas esta feature)
        'multiplier': 1.0,    # Multiplicador global de generación
        'offline_rate': 0.5,  # Tasa de generación cuando el juego está cerrado (50% por defecto)
        'format_precision': 1 # Decimales a mostrar en la UI
    }
}

# Evoluciones y sus requisitos
EVOLUCIONES = {
    1: {
        'nombre': 'Binario a Lenguaje',
        'requisito_nivel': 0,
        'mejoras': {
            1: {'nombre': 'Generador de Datos', 'costo_base': 0, 'cantidad_base': 1.0},
            2: {'nombre': 'Generador de Nivel 1', 'costo_base': 100, 'cantidad_base': 1.0},
            3: {'nombre': 'Generador de Nivel 2', 'costo_base': 1000, 'cantidad_base': 1.0},
            4: {'nombre': 'Generador de Nivel 3', 'costo_base': 10000, 'cantidad_base': 1.0},
            5: {'nombre': 'Generador de Nivel 4', 'costo_base': 100000, 'cantidad_base': 1.0},
        }
    },
    # ... Aquí irían las otras evoluciones ...
}

# Configuración inicial de Kivy
def init_kivy():
    Config.set('input', 'mouse', 'mouse')
    Config.set('graphics', 'width', str(WINDOW_CONFIG['width']))
    Config.set('graphics', 'height', str(WINDOW_CONFIG['height']))