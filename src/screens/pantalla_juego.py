# src/screens/pantalla_juego.py
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget

class PantallaJuego(Screen):
    def __init__(self, game_instance, **kwargs):
        super().__init__(**kwargs)
        self.game = game_instance
        self.botones_mejora = {}
        
        self.layout = BoxLayout(
            orientation='vertical', 
            padding=[5, 5],
            spacing=5
        )
        
        # Stats en esquina
        self.layout.add_widget(self._crear_stats())
        
        # Área de evoluciones
        self.layout.add_widget(self._crear_evoluciones())
        
        # Navegación
        self.layout.add_widget(self._crear_navegacion())
        
        self.add_widget(self.layout)

    def _crear_stats(self):
        stats_container = BoxLayout(
            size_hint_y=0.06,
            padding=[5, 0]
        )
        
        stats_box = BoxLayout(
            size_hint_x=0.4,
            spacing=10
        )
        
        datos_box = BoxLayout(size_hint_x=0.5)
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
        
        dps_box = BoxLayout(size_hint_x=0.5)
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
            size_hint_y=0.8,
            size_hint_x=1,  # Asegurarse de que ocupe todo el ancho
            do_scroll_x=False,
            do_scroll_y=True
        )
        
        self.mejoras_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            size_hint_x=1,  # Asegurarse de que ocupe todo el ancho
            spacing=5,
            padding=[10, 5]
        )
        self.mejoras_container.bind(minimum_height=self.mejoras_container.setter('height'))
        
        # Inicializar mejoras
        self.mejoras_activas = []
        for i in range(4):
            mejora_box = self._crear_slot_mejora(i)
            self.mejoras_activas.append(mejora_box)
            self.mejoras_container.add_widget(mejora_box)
        
        # Label de estado de IA
        self.ia_status = Label(
            text="NUEVA ACTUALIZACIÓN DE IA",
            size_hint_y=None,
            height=40,
            color=(1, 1, 0, 1),
            font_size='16sp',
            bold=True
        )
        self.mejoras_container.add_widget(self.ia_status)
        
        scroll_view.add_widget(self.mejoras_container)
        return scroll_view

    def _crear_slot_mejora(self, index):
        mejora = list(self.game.evoluciones[1].mejoras.values())[index]
        
        # Contenedor principal del slot - importante: size_hint_x = 1
        slot = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),  # Ocupa todo el ancho disponible
            height=100,
            padding=[15, 10],
            spacing=15
        )
        
        # Círculo izquierdo con nivel
        circulo_nivel = Button(
            text=str(mejora.nivel),
            size_hint=(None, None),
            size=(70, 70),
            background_normal='',
            background_color=self._get_color_by_index(index),
            bold=True,
            font_size='24sp',
            disabled=True
        )
        
        # Información central - ajustado el size_hint_x
        info_box = BoxLayout(
            orientation='vertical',
            size_hint_x=0.6,  # Ocupa más espacio
            spacing=5,
            padding=[10, 0]  # Añadido padding horizontal
        )
        
        nombre_label = Label(
            text=mejora.nombre,
            font_size='18sp',
            bold=True,
            halign='left',
            text_size=(None, None),  # Permitir que el texto se ajuste
            color=(1, 1, 1, 1)
        )
        
        generando_label = Label(
            text=f"Generando: {mejora.obtener_generacion():.1f}/s",
            font_size='16sp',
            halign='left',
            text_size=(None, None),  # Permitir que el texto se ajuste
            color=(0.8, 0.8, 0.8, 1)
        )
        
        info_box.add_widget(nombre_label)
        info_box.add_widget(generando_label)
        
        # Botón de compra - ajustado el size_hint_x
        if mejora.id % 4 == 0:
            btn_compra = Button(
                text="DESBLOQUEAR",
                size_hint_x=0.2,  # Ajustado el tamaño
                background_normal='',
                background_color=(0.8, 0.6, 0, 1),
                bold=True
            )
        else:
            btn_compra = Button(
                text="Comprar",
                size_hint_x=0.2,  # Ajustado el tamaño
                background_normal='',
                background_color=(0.2, 0.5, 0.2, 1),
                bold=True
            )
        
        btn_compra.bind(on_press=lambda x: self.game.comprar_mejora(mejora))
        self.botones_mejora[mejora.id] = btn_compra
        
        # Añadir todo al slot
        slot.add_widget(circulo_nivel)
        slot.add_widget(info_box)
        slot.add_widget(btn_compra)
        
        return slot

    def _get_color_by_index(self, index):
        """Retorna un color basado en el índice de la mejora"""
        colors = [
            (0.8, 0.2, 0.2, 1),  # Rojo
            (0.8, 0.4, 0.0, 1),  # Naranja
            (0.2, 0.6, 0.2, 1),  # Verde
            (0.2, 0.4, 0.8, 1),  # Azul
            (0.6, 0.2, 0.6, 1),  # Púrpura
        ]
        return colors[index % len(colors)]

    def desbloquear_nuevas_mejoras(self):
        mejoras_actuales = len(self.mejoras_container.children) - 1
        for i in range(4):
            nuevo_index = mejoras_actuales + i
            if nuevo_index < 20:
                nueva_mejora = self._crear_slot_mejora(nuevo_index)
                self.mejoras_container.add_widget(nueva_mejora, index=0)
        
        self.mejoras_container.remove_widget(self.ia_status)
        self.mejoras_container.add_widget(self.ia_status)

    def _actualizar_color_boton(self, btn, mejora):
        if not mejora.desbloqueada:
            btn.disabled = True
            return

        if mejora.id % 4 == 0:
            if mejora.nivel > 0:
                btn.text = "DESBLOQUEADO"
                btn.disabled = True
                btn.background_color = (0.2, 0.2, 0.2, 1)
            else:
                btn.text = "DESBLOQUEAR"
                btn.disabled = not mejora.puede_comprar(self.game.datos)
                btn.background_color = (0.8, 0.6, 0.0, 1) if mejora.puede_comprar(self.game.datos) else (0.4, 0.3, 0.0, 1)
        else:
            btn.text = "Comprar"
            btn.disabled = not mejora.puede_comprar(self.game.datos)
            btn.background_color = (0.2, 0.6, 0.3, 1) if mejora.puede_comprar(self.game.datos) else (0.6, 0.2, 0.2, 1)

    def actualizar_boton_mejora(self, mejora):
        if mejora.id in self.botones_mejora:
            btn = self.botones_mejora[mejora.id]
            slot = btn.parent
            if slot:
                # Actualizar círculo de nivel
                circulo_nivel = slot.children[2]  # El primer widget
                circulo_nivel.text = str(mejora.nivel)
                
                # Actualizar info de generación
                info_box = slot.children[1]
                generando_label = info_box.children[0]
                generando_label.text = f"Generando: {mejora.obtener_generacion():.1f}/s"
                
                # Actualizar botón de compra
                if mejora.id % 4 == 0:
                    if mejora.nivel > 0:
                        btn.text = "DESBLOQUEADO"
                        btn.disabled = True
                        btn.background_color = (0.3, 0.3, 0.3, 1)
                    else:
                        btn.text = "DESBLOQUEAR"
                        btn.disabled = not mejora.puede_comprar(self.game.datos)
                else:
                    btn.text = f"MEJORAR\nNv.{mejora.nivel}"
                    btn.disabled = not mejora.puede_comprar(self.game.datos)

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
            font_size='16sp'
        )
        
        btn_visual.bind(on_press=lambda x: self.game.cambiar_pantalla('visual'))
        nav_box.add_widget(btn_mejoras)
        nav_box.add_widget(btn_visual)
        return nav_box