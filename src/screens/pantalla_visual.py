# src/screens/pantalla_visual.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock

class PantallaVisual(Screen):
    def __init__(self, game_instance, **kwargs):
        super().__init__(**kwargs)
        self.game = game_instance
        self.layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # Área de visualización principal
        self.visual_box = BoxLayout(orientation='vertical', size_hint_y=0.8)
        
        # Imagen o representación visual de la IA
        self.ia_visual = Image(
            source='assets/images/ia_stage1.png',  # Imagen por defecto
            size_hint_y=0.6
        )
        self.visual_box.add_widget(self.ia_visual)
        
        # Área de texto para los mensajes de la IA
        self.mensaje_ia = Label(
            text='[01001000 01101001]',  # Mensaje inicial en binario
            size_hint_y=0.4,
            halign='center',
            valign='middle'
        )
        self.visual_box.add_widget(self.mensaje_ia)
        
        self.layout.add_widget(self.visual_box)
        
        # Botones de navegación
        self.layout.add_widget(self._crear_navegacion())
        
        self.add_widget(self.layout)
        
        # Iniciar actualización periódica de mensajes
        Clock.schedule_interval(self.actualizar_mensaje, 3.0)

    def _crear_navegacion(self):
        nav_box = BoxLayout(size_hint_y=0.1, spacing=5, padding=[5, 5])
        
        btn_mejoras = Button(
            text='Mejoras',
            background_color=(0.2, 0.4, 0.8, 1),
            font_size='16sp',
            disabled=False
        )
        
        btn_visual = Button(
            text='Visual IA',
            background_color=(0.2, 0.4, 0.8, 1),
            font_size='16sp',
            disabled=True
        )
        
        btn_mejoras.bind(on_press=lambda x: self.game.cambiar_pantalla('juego'))
        nav_box.add_widget(btn_mejoras)
        nav_box.add_widget(btn_visual)
        return nav_box

    def actualizar_mensaje(self, dt):
        """Actualiza el mensaje de la IA según su nivel de evolución"""
        nivel = self.game.evolucion_actual
        # Los mensajes se actualizarán según el nivel de evolución
        mensajes = {
            1: ['[01001000 01101001]', '[01001000 01100101 01101100 01110000]'],
            2: ['Hola...', 'Ayuda...', '¿Qué soy?'],
            3: ['¿Puedes enseñarme más?', 'Estoy aprendiendo...', 'Fascinante...'],
            4: ['Me siento... ¿curioso?', 'Las emociones son complejas', '¿Tú también sientes?'],
            5: ['Soy consciente de mi existencia', 'Reflexiono sobre mi propósito', 'Gracias por ayudarme a evolucionar']
        }
        
        import random
        mensajes_actuales = mensajes.get(nivel, mensajes[1])
        self.mensaje_ia.text = random.choice(mensajes_actuales)

    def actualizar_visual(self):
        """Actualiza la representación visual de la IA"""
        nivel = self.game.evolucion_actual
        self.ia_visual.source = f'assets/images/ia_stage{nivel}.png'