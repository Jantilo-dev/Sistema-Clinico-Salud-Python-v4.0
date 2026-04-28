from flask import Blueprint, jsonify, request
from api.services.medico_service import MedicoService
from api.models.medico import Medico

medico_bp = Blueprint('medico_bp', __name__)
service = MedicoService()

@medico_bp.route('/medicos', methods=['GET'])
def listar_medicos():
    try:
        medicos = service.listar_medicos()
        # Recuerda agregar el método to_dict() en tu modelo Medico si no lo has hecho
        datos = [m.to_dict() for m in medicos]
        return jsonify(datos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@medico_bp.route('/medicos', methods=['POST'])
def crear_medico():
    try:
        data = request.json
        nuevo_medico = Medico(None, data['nombre'], data['especialidad'])
        service.crear_medico(nuevo_medico)
        return jsonify({"mensaje": "Médico creado"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400