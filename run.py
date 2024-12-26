from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import time
import os
import sys

class MyHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.restart_program()

    def restart_program(self):
        if self.process:
            self.process.kill()
        # Usar el ejecutable de Python del entorno virtual
        python_exe = sys.executable
        self.process = subprocess.Popen([python_exe, 'main.py'])

    def on_modified(self, event):
        if event.src_path.endswith('main.py'):
            print("Cambios detectados, reiniciando...")
            self.restart_program()

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        if event_handler.process:
            event_handler.process.kill()
    observer.join()