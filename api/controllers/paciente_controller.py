from flask import Blueprint, jsonify, request
from api.services.paciente_service import PacienteService
from api.models.paciente import Paciente

# Creamos un "Blueprint" (es como una sección de la app)
paciente_bp = Blueprint('paciente_bp', __name__)
service = PacienteService()

@paciente_bp.route('/pacientes', methods=['GET'])
def listar_pacientes_api():
    """URL: http://localhost:5000/api/pacientes"""
    try:
        pacientes = service.listar_pacientes()
        # Convertimos la lista de objetos a lista de diccionarios (JSON)
        datos_json = [p.to_dict() for p in pacientes]
        return jsonify(datos_json), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@paciente_bp.route('/pacientes', methods=['POST'])
def crear_paciente_api():
    """Permite crear un paciente enviando JSON"""
    try:
        datos = request.json
        nuevo_paciente = Paciente(None, datos['nombre'], datos['rut'], datos['telefono'])
        service.crear_paciente(nuevo_paciente)
        return jsonify({"mensaje": "Paciente creado con éxito"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400