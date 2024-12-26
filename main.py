from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty
from kivy.config import Config

# Configuración inicial de la ventana
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '600')

class IdleAwakening(BoxLayout):
    # Recursos básicos
    datos = NumericProperty(0)
    datos_por_segundo = NumericProperty(1)
    nivel_consciencia = NumericProperty(1)
    pensamientos = StringProperty("01001... procesando datos básicos...")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 15
        self.spacing = 10
        
        # Título del juego
        self.titulo = Label(
            text='Idle Awakening',
            font_size='24sp',
            size_hint_y=0.1
        )
        self.add_widget(self.titulo)
        
        # Panel de estadísticas
        self.stats_box = BoxLayout(
            orientation='vertical',
            size_hint_y=0.2,
            spacing=5
        )
        self.datos_label = Label(text=f'Datos: {self.datos}')
        self.dps_label = Label(text=f'Datos/s: {self.datos_por_segundo}')
        self.nivel_label = Label(text=f'Nivel de Consciencia: {self.nivel_consciencia}')
        
        for label in [self.datos_label, self.dps_label, self.nivel_label]:
            self.stats_box.add_widget(label)
        self.add_widget(self.stats_box)
        
        # Panel de pensamientos de la IA
        self.pensamiento_box = BoxLayout(
            orientation='vertical',
            size_hint_y=0.3,
            padding=10
        )
        self.pensamiento_title = Label(
            text='Estado Mental:',
            size_hint_y=0.3
        )
        self.pensamiento_label = Label(
            text=self.pensamientos,
            size_hint_y=0.7
        )
        self.pensamiento_box.add_widget(self.pensamiento_title)
        self.pensamiento_box.add_widget(self.pensamiento_label)
        self.add_widget(self.pensamiento_box)
        
        # Módulos de mejora
        self.modulos_box = BoxLayout(
            orientation='vertical',
            size_hint_y=0.4,
            spacing=10
        )
        
        self.modulo_procesamiento = Button(
            text='Mejorar Procesamiento\nCosto: 10 datos',
            on_press=self.mejorar_procesamiento
        )
        self.modulo_memoria = Button(
            text='Expandir Memoria\nCosto: 25 datos',
            on_press=self.mejorar_memoria
        )
        
        self.modulos_box.add_widget(self.modulo_procesamiento)
        self.modulos_box.add_widget(self.modulo_memoria)
        self.add_widget(self.modulos_box)
        
        # Iniciar el bucle del juego
        Clock.schedule_interval(self.actualizar, 1.0)
    
    def actualizar(self, dt):
        self.datos += self.datos_por_segundo
        self.actualizar_labels()
        
    def actualizar_labels(self):
        self.datos_label.text = f'Datos: {int(self.datos)}'
        self.dps_label.text = f'Datos/s: {self.datos_por_segundo}'
        self.nivel_label.text = f'Nivel de Consciencia: {self.nivel_consciencia}'
        
    def mejorar_procesamiento(self, instance):
        if self.datos >= 10:
            self.datos -= 10
            self.datos_por_segundo += 1
            self.actualizar_labels()
            
    def mejorar_memoria(self, instance):
        if self.datos >= 25:
            self.datos -= 25
            self.datos_por_segundo += 3
            self.actualizar_labels()

class IdleAwakeningApp(App):
    def build(self):
        return IdleAwakening()

if __name__ == '__main__':
    IdleAwakeningApp().run()