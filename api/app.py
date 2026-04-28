import sys
import os

# Ajuste de ruta para ejecutar desde VS Code o Terminal
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(base_dir)

from flask import Flask
# Importamos los 3 controladores
from api.controllers.paciente_controller import paciente_bp
from api.controllers.medico_controller import medico_bp
from api.controllers.cita_controller import cita_bp

app = Flask(__name__)

# Registramos las rutas
app.register_blueprint(paciente_bp, url_prefix='/api')
app.register_blueprint(medico_bp, url_prefix='/api')
app.register_blueprint(cita_bp, url_prefix='/api')

if __name__ == '__main__':
    print(" API corriendo en http://localhost:5000")
    print("Rutas disponibles:")
    print(" - http://localhost:5000/api/pacientes")
    print(" - http://localhost:5000/api/medicos")
    print(" - http://localhost:5000/api/citas")
    app.run(debug=True, port=5000)