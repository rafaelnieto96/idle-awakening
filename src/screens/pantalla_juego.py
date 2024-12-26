# src/screens/pantalla_juego.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

class PantallaJuego(Screen):
    def __init__(self, game_instance, **kwargs):
        super().__init__(**kwargs)
        self.game = game_instance
        
        # Layout principal
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        # Añadir componentes
        self.layout.add_widget(self._crear_header())
        self.layout.add_widget(self._crear_stats())
        self.layout.add_widget(self._crear_evoluciones())
        self.layout.add_widget(self._crear_navegacion())
        
        self.add_widget(self.layout)

    def _crear_header(self):
        titulo_box = BoxLayout(size_hint_y=0.1, padding=[0, 5])
        titulo_box.add_widget(Label(
            text='Idle Awakening',
            font_size='24sp',
            bold=True,
            color=(0.9, 0.9, 1, 1)
        ))
        return titulo_box

    def _crear_stats(self):
        self.stats_box = BoxLayout(
            orientation='vertical',
            size_hint_y=0.15,
            padding=[10, 5],
            spacing=2
        )
        
        # Crear labels para estadísticas
        self.datos_label = Label(
            text=f'Datos: {self.game.datos}',
            font_size='18sp',
            halign='left'
        )
        self.dps_label = Label(
            text=f'Datos/s: {self.game.datos_por_segundo}',
            font_size='18sp',
            halign='left'
        )
        self.nivel_label = Label(
            text=f'Evolución: {self.game.evolucion_actual}',
            font_size='18sp',
            halign='left'
        )
        
        for label in [self.datos_label, self.dps_label, self.nivel_label]:
            self.stats_box.add_widget(label)
            
        return self.stats_box

    def _crear_evoluciones(self):
      # Contenedor principal con scroll
      scroll_view = ScrollView(size_hint_y=0.65)
      
      # BoxLayout principal para todo el contenido
      self.evoluciones_box = BoxLayout(
          orientation='vertical',
          size_hint_y=None,  # Necesario para scroll
          spacing=10,
          padding=[5, 5]
      )
      
      # Para cada evolución
      for evolucion in self.game.evoluciones.values():
          # Título de la evolución
          titulo = Label(
              text=f"Evolución {evolucion.id}: {evolucion.nombre}",
              size_hint_y=None,
              height=40,  # Altura fija para el título
              font_size='18sp',
              bold=True
          )
          self.evoluciones_box.add_widget(titulo)
          
          # Añadir botones de mejoras
          for mejora in evolucion.mejoras.values():
              # Botón de mejora
              btn = Button(
                  text=mejora.obtener_descripcion(),
                  size_hint_y=None,  # Importante para el scroll
                  height=80,  # Altura fija para cada botón
                  background_color=(0.3, 0.3, 0.35, 1) if mejora.desbloqueada else (0.2, 0.2, 0.2, 1)
              )
              btn.bind(on_press=lambda x, m=mejora: self.game.comprar_mejora(m))
              self.evoluciones_box.add_widget(btn)

      # Este binding es crucial - ajusta la altura total del contenido
      self.evoluciones_box.bind(minimum_height=self.evoluciones_box.setter('height'))
      scroll_view.add_widget(self.evoluciones_box)
      return scroll_view

    def _crear_navegacion(self):
        nav_box = BoxLayout(size_hint_y=0.1, spacing=5, padding=[5, 5])
        
        btn_mejoras = Button(
            text='Mejoras',
            background_color=(0.2, 0.4, 0.8, 1),
            font_size='16sp',
            disabled=True
        )
        
        btn_visual = Button(
            text='Visual IA',
            background_color=(0.2, 0.4, 0.8, 1),
            font_size='16sp',
            disabled=False
        )
        
        btn_visual.bind(on_press=lambda x: self.game.cambiar_pantalla('visual'))
        nav_box.add_widget(btn_mejoras)
        nav_box.add_widget(btn_visual)
        return nav_box

    def actualizar(self):
        """Actualiza todos los elementos de la UI"""
        self.datos_label.text = f'Datos: {int(self.game.datos)}'
        self.dps_label.text = f'Datos/s: {self.game.datos_por_segundo}'
        self.nivel_label.text = f'Evolución: {self.game.evolucion_actual}'
        
        # Actualizar estado de las mejoras
        for evolucion in self.game.evoluciones.values():
            for mejora in evolucion.mejoras.values():
                # Aquí podrías actualizar el estado visual de cada mejora
                pass