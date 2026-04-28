from api.models.persona import Persona

class Medico(Persona):
    def __init__(self, id_medico, nombre, especialidad):
        super().__init__(id_medico, nombre)
        self._especialidad = especialidad

    @property
    def especialidad(self):
        return self._especialidad

    # Polimorfismo: Para mostrar en consola (Main.py)
    def mostrar_info(self):
        return f"[MÉDICO] Dr/a. {self._nombre} - Especialidad: {self._especialidad}"
    
    # --- ESTE ES EL MÉTODO QUE FALTABA ---
    # Serialización: Para enviar por API (App.py)
    def to_dict(self):
        return {
            "id": self._id,
            "nombre": self._nombre,
            "especialidad": self._especialidad
        }