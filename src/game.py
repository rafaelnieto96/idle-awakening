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
    datos = NumericProperty(0)
    datos_por_segundo = NumericProperty(1)
    evolucion_actual = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
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
        """Inicializa todas las evoluciones y sus mejoras"""
        for id_evolucion, datos in EVOLUCIONES.items():
            mejoras = {}
            for id_mejora, mejora_data in datos['mejoras'].items():
                mejoras[id_mejora] = Mejora(
                    mejora_data['nombre'],
                    mejora_data['costo_base'],
                    mejora_data['incremento_dps']
                )
            
            self.evoluciones[id_evolucion] = Evolucion(
                id_evolucion,
                datos['nombre'],
                datos['requisito_nivel'],
                mejoras
            )
            
        # Desbloquear primera evolución
        self.evoluciones[1].desbloqueada = True
        for mejora in self.evoluciones[1].mejoras.values():
            mejora.desbloqueada = True

    def actualizar(self, dt):
        """Actualización principal del juego"""
        self.datos += self.datos_por_segundo
        self.verificar_evoluciones()
        self.pantalla_juego.actualizar()
        
    def comprar_mejora(self, mejora):
        """Intenta comprar una mejora"""
        if mejora.puede_comprar(self.datos):
            costo = mejora.calcular_costo()
            self.datos -= costo
            self.datos_por_segundo += mejora.incremento_dps
            mejora.nivel += 1
            
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