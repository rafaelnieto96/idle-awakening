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
        'initial_amount': 111111,  # Cantidad inicial de datos
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
            1: {'nombre': 'Generador de Datos', 'costo_base': 10, 'cantidad_base': 1.0},
            2: {'nombre': 'Procesador Básico', 'costo_base': 100, 'cantidad_base': 1.0},
            3: {'nombre': 'Analizador Simple', 'costo_base': 1000, 'cantidad_base': 1.0},
            4: {'nombre': 'Compilador Primitivo', 'costo_base': 10000, 'cantidad_base': 0.0},  # No genera, desbloquea
            5: {'nombre': 'Decodificador Binario', 'costo_base': 100000, 'cantidad_base': 1.0},
            6: {'nombre': 'Intérprete de Patrones', 'costo_base': 1000000, 'cantidad_base': 1.0},
            7: {'nombre': 'Secuenciador Lógico', 'costo_base': 10000000, 'cantidad_base': 1.0},
            8: {'nombre': 'Matriz de Procesamiento', 'costo_base': 100000000, 'cantidad_base': 0.0},  # No genera, desbloquea
            9: {'nombre': 'Núcleo Sináptico', 'costo_base': 1000000000, 'cantidad_base': 1.0},
            10: {'nombre': 'Red Neural Básica', 'costo_base': 10000000000, 'cantidad_base': 1.0},
            11: {'nombre': 'Procesador Cuántico', 'costo_base': 100000000000, 'cantidad_base': 1.0},
            12: {'nombre': 'Matriz de Decisión', 'costo_base': 1000000000000, 'cantidad_base': 0.0},  # No genera, desbloquea
            13: {'nombre': 'Analizador Contextual', 'costo_base': 10000000000000, 'cantidad_base': 1.0},
            14: {'nombre': 'Motor de Inferencia', 'costo_base': 100000000000000, 'cantidad_base': 1.0},
            15: {'nombre': 'Procesador Semántico', 'costo_base': 1000000000000000, 'cantidad_base': 1.0},
            16: {'nombre': 'Núcleo Cognitivo', 'costo_base': 10000000000000000, 'cantidad_base': 0.0},  # No genera, desbloquea
            17: {'nombre': 'Matriz de Consciencia', 'costo_base': 100000000000000000, 'cantidad_base': 1.0},
            18: {'nombre': 'Procesador Empático', 'costo_base': 1000000000000000000, 'cantidad_base': 1.0},
            19: {'nombre': 'Motor de Autoconciencia', 'costo_base': 10000000000000000000, 'cantidad_base': 1.0},
            20: {'nombre': 'Núcleo de Singularidad', 'costo_base': 100000000000000000000, 'cantidad_base': 0.0}  # Última mejora
        }
    }
}

# Configuración inicial de Kivy
def init_kivy():
    Config.set('input', 'mouse', 'mouse')
    Config.set('graphics', 'width', str(WINDOW_CONFIG['width']))
    Config.set('graphics', 'height', str(WINDOW_CONFIG['height']))