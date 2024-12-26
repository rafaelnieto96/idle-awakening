# main.py
from src.config.settings import init_kivy
from src.game import IdleAwakeningApp
from kivy.core.window import Window

init_kivy()

if __name__ == '__main__':
    IdleAwakeningApp().run()