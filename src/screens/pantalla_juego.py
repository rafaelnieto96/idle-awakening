# src/screens/pantalla_juego.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget

class PantallaJuego(Screen):
    def __init__(self, game_instance, **kwargs):
      super().__init__(**kwargs)
      self.game = game_instance
      
      # Layout principal con menos padding para hacer la pantalla más rectangular
      self.layout = BoxLayout(
          orientation='vertical', 
          padding=[5, 5],  # Reducido el padding
          spacing=5
      )
      
      # Stats en esquina
      self.layout.add_widget(self._crear_stats())
      
      # Área de evoluciones
      self.layout.add_widget(self._crear_evoluciones())
      
      # Navegación
      self.layout.add_widget(self._crear_navegacion())
      
      self.add_widget(self.layout)

    def _crear_header_con_stats(self):
      header = BoxLayout(
          size_hint_y=0.1, 
          spacing=10
      )
      
      # Título
      header.add_widget(Label(
          text='Idle Awakening',
          font_size='24sp',
          bold=True,
          size_hint_x=0.6,
          color=(0.9, 0.9, 1, 1)
      ))
      
      # Stats en la esquina
      stats_box = BoxLayout(
          orientation='vertical',
          size_hint_x=0.4,
          padding=[5, 0]
      )
      
      self.datos_label = Label(
          text=f'{int(self.game.datos)} datos',
          font_size='14sp',
          halign='right'
      )
      self.dps_label = Label(
          text=f'{self.game.datos_por_segundo}/s',
          font_size='14sp',
          halign='right'
      )
      self.nivel_label = Label(
          text=f'Evolución {self.game.evolucion_actual}',
          font_size='14sp',
          halign='right'
      )
      
      for label in [self.datos_label, self.dps_label, self.nivel_label]:
          stats_box.add_widget(label)
      
      header.add_widget(stats_box)
      return header
    
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
      stats_container = BoxLayout(
          size_hint_y=0.06,
          padding=[5, 0]
      )
      
      # Stats box alineado a la izquierda
      stats_box = BoxLayout(
          size_hint_x=0.4,
          spacing=10
      )
      
      # Box para datos
      datos_box = BoxLayout(
          size_hint_x=0.5
      )
      self.datos_label = Label(
          text=f'{int(self.game.datos)}',
          font_size='14sp',
          halign='right'
      )
      datos_text = Label(
          text='Datos',
          font_size='16sp',
          halign='left'
      )
      datos_box.add_widget(self.datos_label)
      datos_box.add_widget(datos_text)
      
      # Box para datos por segundo
      dps_box = BoxLayout(
          size_hint_x=0.5
      )
      self.dps_label = Label(
          text=f'{self.game.datos_por_segundo}',
          font_size='14sp',
          halign='right'
      )

      dps_box.add_widget(self.dps_label)
      
      stats_box.add_widget(datos_box)
      stats_box.add_widget(dps_box)
      
      stats_container.add_widget(stats_box)
      stats_container.add_widget(Widget())
      
      return stats_container

    def _crear_evoluciones(self):
      scroll_view = ScrollView(
          size_hint_y=0.84,
          do_scroll_x=False,
          do_scroll_y=True
      )
      
      # Layout principal de evoluciones
      self.evoluciones_box = BoxLayout(
          orientation='vertical',
          size_hint_y=None,
          spacing=10,
          padding=[5, 5]
      )
      
      # Diccionario para guardar los botones
      self.botones_mejora = {}
      
      for evolucion in self.game.evoluciones.values():
          for mejora in evolucion.mejoras.values():
              btn = self._crear_boton_mejora(mejora)
              self.botones_mejora[mejora.id] = btn
              self.evoluciones_box.add_widget(btn)
      
      # Esto es crucial para que el scroll funcione correctamente
      self.evoluciones_box.bind(minimum_height=self.evoluciones_box.setter('height'))
      scroll_view.add_widget(self.evoluciones_box)
      
      return scroll_view

    def _crear_boton_mejora(self, mejora):
        btn = Button(
            text=f"{mejora.nombre}\n"
            f"Nivel: {mejora.nivel} - Costo: {mejora.calcular_costo()} datos\n"
            f"Generando: {mejora.cantidad:.1f}/s",
            size_hint_y=None,
            height=60,
            background_color=(0.3, 0.3, 0.35, 1) if mejora.desbloqueada else (0.2, 0.2, 0.2, 1),
            halign='center'
        )
        btn.bind(on_press=lambda x, m=mejora: self.game.comprar_mejora(m))
        return btn

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

    def comprar_mejora(self, mejora):
        if mejora.puede_comprar(self.datos):
            costo = mejora.calcular_costo()
            self.datos -= costo
            mejora.nivel += 1
            # Actualizar el botón específico
            self.pantalla_juego.actualizar_boton_mejora(mejora)
    
    def actualizar_boton_mejora(self, mejora):
      if mejora.id in self.botones_mejora:
          btn = self.botones_mejora[mejora.id]
          btn.text = (f"{mejora.nombre}\n"
                    f"Nivel: {mejora.nivel} - Costo: {mejora.calcular_costo()} datos\n"
                    f"Generando: {mejora.cantidad:.1f}/s\n"
                    f"Disponible: {mejora.cantidad_disponible:.1f}")

    def actualizar_mejoras(self):
      for mejora_id, btn in self.botones_mejora.items():
          mejora = self.game.evoluciones[1].mejoras[mejora_id]
          self.actualizar_boton_mejora(mejora)
          
      # Actualizar también los stats
      self.datos_label.text = f'{int(self.game.datos)}'
      self.dps_label.text = f'{self.game.datos_por_segundo}/s'