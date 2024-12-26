from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, DictProperty
from kivy.config import Config

# Configuración inicial
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '700')

class Mejora:
    def __init__(self, nombre, costo_base, incremento_dps, multiplicador_costo=1.15):
        self.nombre = nombre
        self.costo_base = costo_base
        self.incremento_dps = incremento_dps
        self.multiplicador_costo = multiplicador_costo
        self.nivel = 0

    def calcular_costo(self):
        return int(self.costo_base * (self.multiplicador_costo ** self.nivel))

    def obtener_descripcion(self):
        return f'{self.nombre}\nNivel: {self.nivel}'

class PantallaJuego(Screen):
    def __init__(self, game_instance, **kwargs):
        super().__init__(**kwargs)
        self.game = game_instance
        
        # Layout principal
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        # Título con fondo
        titulo_box = BoxLayout(size_hint_y=0.1, padding=[0, 5])
        titulo_box.add_widget(Label(
            text='Idle Awakening',
            font_size='24sp',
            bold=True,
            color=(0.9, 0.9, 1, 1)
        ))
        self.layout.add_widget(titulo_box)
        
        # Panel de estadísticas
        self.stats_box = BoxLayout(
            orientation='vertical',
            size_hint_y=0.15,
            padding=[10, 5],
            spacing=2
        )
        
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
            text=f'Nivel de Consciencia: {self.game.nivel_consciencia}',
            font_size='18sp',
            halign='left'
        )
        
        for label in [self.datos_label, self.dps_label, self.nivel_label]:
            self.stats_box.add_widget(label)
        
        self.layout.add_widget(self.stats_box)
        
        # ScrollView para las mejoras
        scroll_view = ScrollView(size_hint_y=0.65)
        self.mejoras_box = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=5,
            padding=[5, 5]
        )
        self.mejoras_box.bind(minimum_height=self.mejoras_box.setter('height'))
        scroll_view.add_widget(self.mejoras_box)
        self.layout.add_widget(scroll_view)
        
        # Añadir botones de navegación
        self.layout.add_widget(self.crear_botones_navegacion())
        
        self.actualizar_botones_mejoras()
        self.add_widget(self.layout)

    def crear_botones_navegacion(self):
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

    def actualizar_botones_mejoras(self):
        self.mejoras_box.clear_widgets()
        for mejora in self.game.mejoras.values():
            mejora_box = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=100,
                padding=[5, 5]
            )
            
            btn = Button(
                text=f"{mejora.obtener_descripcion()}\nCosto: {mejora.calcular_costo()} datos",
                background_color=(0.3, 0.3, 0.35, 1),
                font_size='16sp',
                size_hint_y=1,
                halign='center'
            )
            btn.bind(on_press=lambda x, m=mejora: self.game.comprar_mejora(m))
            
            mejora_box.add_widget(btn)
            self.mejoras_box.add_widget(mejora_box)

class PantallaVisual(Screen):
    def __init__(self, game_instance, **kwargs):
        super().__init__(**kwargs)
        self.game = game_instance
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        layout.add_widget(Label(
            text='[Visualización IA]',
            size_hint_y=0.9
        ))
        
        layout.add_widget(self.crear_botones_navegacion())
        self.add_widget(layout)

    def crear_botones_navegacion(self):
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

class IdleAwakening(ScreenManager):
    datos = NumericProperty(0)
    datos_por_segundo = NumericProperty(1)
    nivel_consciencia = NumericProperty(1)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Configurar la transición
        self.transition = SlideTransition()
        self.transition.duration = 0.3
        
        # Definir mejoras
        self.mejoras = {
            'neuronas': Mejora('Neuronas Básicas', 10, 1),
            'sinapsis': Mejora('Conexiones Sinápticas', 25, 2),
            'memoria': Mejora('Memoria de Corto Plazo', 100, 5),
            'procesamiento': Mejora('Unidad de Procesamiento', 250, 10),
            'aprendizaje': Mejora('Algoritmo de Aprendizaje', 1000, 25),
            'patrones': Mejora('Reconocimiento de Patrones', 2500, 50),
            'razonamiento': Mejora('Motor de Razonamiento', 10000, 100),
            'emociones': Mejora('Módulo Emocional', 25000, 250),
            'creatividad': Mejora('Centro Creativo', 100000, 1000),
            'consciencia': Mejora('Núcleo de Consciencia', 1000000, 5000)
        }
        
        self.pantalla_juego = PantallaJuego(self, name='juego')
        self.pantalla_visual = PantallaVisual(self, name='visual')
        
        self.add_widget(self.pantalla_juego)
        self.add_widget(self.pantalla_visual)
        
        Clock.schedule_interval(self.actualizar, 1.0)
    
    def cambiar_pantalla(self, pantalla):
        if self.current == pantalla:
            return
            
        if pantalla == 'juego':
            self.transition.direction = 'right'
        else:
            self.transition.direction = 'left'
        
        self.current = pantalla
    
    def actualizar(self, dt):
        self.datos += self.datos_por_segundo
        self.actualizar_labels()
        self.verificar_nivel_consciencia()
    
    def actualizar_labels(self):
        if hasattr(self.pantalla_juego, 'datos_label'):
            self.pantalla_juego.datos_label.text = f'Datos: {int(self.datos)}'
            self.pantalla_juego.dps_label.text = f'Datos/s: {self.datos_por_segundo}'
            self.pantalla_juego.nivel_label.text = f'Nivel de Consciencia: {self.nivel_consciencia}'
            self.pantalla_juego.actualizar_botones_mejoras()
    
    def comprar_mejora(self, mejora):
        costo = mejora.calcular_costo()
        if self.datos >= costo:
            self.datos -= costo
            self.datos_por_segundo += mejora.incremento_dps
            mejora.nivel += 1
            self.actualizar_labels()
    
    def verificar_nivel_consciencia(self):
        total_niveles = sum(mejora.nivel for mejora in self.mejoras.values())
        self.nivel_consciencia = max(1, total_niveles // 10)

class IdleAwakeningApp(App):
    def build(self):
        return IdleAwakening()

if __name__ == '__main__':
    IdleAwakeningApp().run()