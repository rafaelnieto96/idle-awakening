# Crear el entorno virtual
python3 -m venv venv

# Activar entorno virtual: Mac
source venv/bin/activate

# Activar entorno virtual: Windows
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

python main.py
