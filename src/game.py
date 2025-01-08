# src/game.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.clock import Clock
from kivy.properties import NumericProperty

from src.config.settings import EVOLUCIONES, GAME_CONFIG
from src.models.evolucion import Evolucion
from src.models.mejora import Mejora
from src.screens.pantalla_juego import PantallaJuego
from src.screens.pantalla_visual import PantallaVisual

class IdleAwakening(ScreenManager):
    # Definir las propiedades numéricas
    datos = NumericProperty(0)
    datos_por_segundo = NumericProperty(1)
    evolucion_actual = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Inicializar datos con el valor configurado
        self.datos = GAME_CONFIG['currency']['initial_amount']
        self.datos_por_segundo = 1
        self.multiplicador_global = GAME_CONFIG['currency']['multiplier']
        
        # Configurar transición
        self.transition = SlideTransition()
        self.transition.duration = GAME_CONFIG['transition_duration']
        
        # Inicializar evoluciones
        self.evoluciones = {}
        self._inicializar_evoluciones()
        
        # Crear y añadir pantallas
        self.pantalla_juego = PantallaJuego(self, name='juego')
        self.pantalla_visual = PantallaVisual(self, name='visual')
        
        self.add_widget(self.pantalla_juego)
        self.add_widget(self.pantalla_visual)
        
        # Iniciar bucle del juego
        Clock.schedule_interval(self.actualizar, GAME_CONFIG['update_interval'])

    def _inicializar_evoluciones(self):
        for id_evolucion, datos in EVOLUCIONES.items():
            mejoras = {}
            for id_mejora, mejora_data in datos['mejoras'].items():
                mejoras[id_mejora] = Mejora(
                    id_mejora,
                    mejora_data['nombre'],
                    mejora_data['costo_base'],
                    mejora_data['cantidad_base']
                )
            
            self.evoluciones[id_evolucion] = Evolucion(
                id_evolucion,
                datos['nombre'],
                datos['requisito_nivel'],
                mejoras
            )
            
        # Desbloquear solo las primeras 4 mejoras inicialmente
        self.evoluciones[1].desbloqueada = True
        for i in range(1, 5):
            self.evoluciones[1].mejoras[i].desbloqueada = True

    def actualizar(self, dt):
        mejoras = list(self.evoluciones[1].mejoras.values())
        
        # Procesamos desde la última mejora hacia abajo
        for i in range(len(mejoras)-1, 0, -1):
            mejora_actual = mejoras[i]
            mejora_anterior = mejoras[i-1]
            
            # Calcular cuánto genera esta mejora por segundo
            mejora_actual.cantidad = mejora_actual.obtener_generacion()
            
            # Si no es mejora de desbloqueo, actualizar la cantidad disponible de la anterior
            if mejora_actual.id % 4 != 0:
                mejora_anterior.cantidad_disponible += mejora_actual.cantidad * dt
        
        # Procesamos mejora1 (generación de datos)
        mejora1 = mejoras[0]
        generacion_base = mejora1.obtener_generacion()
        generacion_por_disponible = mejora1.cantidad_disponible
        
        # La cantidad total que genera por segundo con el multiplicador global
        mejora1.cantidad = (generacion_base + generacion_por_disponible) * self.multiplicador_global
        
        # Generamos los datos
        self.datos += mejora1.cantidad * dt
        self.datos_por_segundo = mejora1.cantidad

    def _actualizar_ui(self):
        if hasattr(self, 'pantalla_juego'):
            self.pantalla_juego.datos_label.text = f'{int(self.datos)}'
            self.pantalla_juego.dps_label.text = f'{self.datos_por_segundo:.1f}/s'
            
            for mejora_id, mejora in self.evoluciones[1].mejoras.items():
                if mejora_id in self.pantalla_juego.botones_mejora:
                    self.pantalla_juego.actualizar_boton_mejora(mejora)
                    self.pantalla_juego._actualizar_color_boton(
                        self.pantalla_juego.botones_mejora[mejora_id], 
                        mejora
                    )

    def comprar_mejora(self, mejora):
        """Intenta comprar una mejora"""
        if mejora.puede_comprar(self.datos):
            costo = mejora.calcular_costo()
            self.datos -= costo
            mejora.nivel += 1
            
            # Si es una mejora de desbloqueo (4, 8, 12, 16)
            if mejora.id % 4 == 0 and mejora.id < 20:
                # Desbloquear las siguientes 4 mejoras
                for i in range(mejora.id + 1, min(mejora.id + 5, 21)):
                    if i in self.evoluciones[1].mejoras:
                        self.evoluciones[1].mejoras[i].desbloqueada = True
                # Actualizar la UI para mostrar las nuevas mejoras
                self.pantalla_juego.desbloquear_nuevas_mejoras()
                
            # Forzar actualización de UI después de la compra
            self._actualizar_ui()

    def _desbloquear_siguientes_mejoras(self, id_mejora_actual):
        # Desbloquear las siguientes 4 mejoras sin marcarlas como compradas
        for i in range(id_mejora_actual + 1, min(id_mejora_actual + 5, 21)):
            if i in self.evoluciones[1].mejoras:
                mejora = self.evoluciones[1].mejoras[i]
                mejora.desbloqueada = True
                # No modificar el nivel aquí
        
        # Actualizar UI para mostrar nuevas mejoras
        self.pantalla_juego.desbloquear_nuevas_mejoras()

    def verificar_evoluciones(self):
        """Verifica si se puede desbloquear una nueva evolución"""
        for evolucion in self.evoluciones.values():
            if not evolucion.desbloqueada and evolucion.id > 1:
                evolucion_anterior = self.evoluciones[evolucion.id - 1]
                if evolucion_anterior.nivel_total() >= evolucion.requisito_nivel:
                    evolucion.verificar_desbloqueo(evolucion_anterior.nivel_total())
                    if evolucion.desbloqueada:
                        self.evolucion_actual = evolucion.id
                        
    def cambiar_pantalla(self, pantalla):
        """Cambia entre pantallas con la animación correcta"""
        if self.current == pantalla:
            return
        
        self.transition.direction = 'right' if pantalla == 'juego' else 'left'
        self.current = pantalla

class IdleAwakeningApp(App):
    def build(self):
        return IdleAwakening()