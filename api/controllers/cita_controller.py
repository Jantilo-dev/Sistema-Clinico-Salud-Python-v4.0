from flask import Blueprint, jsonify, request
from api.services.cita_service import CitaService
from api.models.cita import Cita

cita_bp = Blueprint('cita_bp', __name__)
service = CitaService()

@cita_bp.route('/citas', methods=['GET'])
def listar_citas():
    try:
        # Usamos el reporte que trae los nombres (Join) para que el JSON sea legible
        citas = service.obtener_reporte_citas() 
        return jsonify(citas), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cita_bp.route('/citas', methods=['POST'])
def agendar_cita():
    try:
        data = request.json

        nueva_cita = Cita(
            None, 
            data['id_paciente'], 
            data['id_medico'], 
            data['fecha'], 
            data['hora'], 
            data['motivo']
        )
        service.agendar_cita(nueva_cita)
        return jsonify({"mensaje": "Cita agendada"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400