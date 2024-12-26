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
            
        # Desbloquear primera evolución
        self.evoluciones[1].desbloqueada = True
        for mejora in self.evoluciones[1].mejoras.values():
            mejora.desbloqueada = True

    def actualizar(self, dt):
        mejoras = list(self.evoluciones[1].mejoras.values())
        
        # La primera mejora genera datos directamente por su nivel
        mejoras[0].cantidad = mejoras[0].obtener_generacion()
        self.datos += mejoras[0].cantidad * dt
        
        # Ahora procesamos las generaciones en cascada
        for i in range(len(mejoras)-1, 0, -1):
            # Cada mejora genera unidades de la mejora anterior
            mejora_actual = mejoras[i]
            mejora_anterior = mejoras[i-1]
            
            # Generar mejoras del nivel anterior
            generado = mejora_actual.obtener_generacion() * dt
            mejora_anterior.cantidad_disponible += generado
            
            # La cantidad por segundo es la suma de su propia generación más lo que recibe
            mejora_anterior.cantidad = mejora_anterior.obtener_generacion()
        
        # Actualizar datos por segundo
        self.datos_por_segundo = mejoras[0].cantidad
        
        # Actualizar UI
        self.pantalla_juego.actualizar_mejoras()
        
    def comprar_mejora(self, mejora):
        """Intenta comprar una mejora"""
        if mejora.puede_comprar(self.datos):
            costo = mejora.calcular_costo()
            self.datos -= costo
            mejora.nivel += 1
            self.pantalla_juego.actualizar_mejoras()
            
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