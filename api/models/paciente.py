# api/models/paciente.py
from api.models.persona import Persona

class Paciente(Persona): # Herencia
    def __init__(self, id_paciente, nombre, rut, telefono):
        super().__init__(id_paciente, nombre) # Constructor del padre
        self._rut = rut
        self._telefono = telefono

    @property
    def rut(self):
        return self._rut

    @property
    def telefono(self):
        return self._telefono

    # Polimorfismo: Sobreescritura de método
    def mostrar_info(self):
        base_info = super().mostrar_info()
        return f"[PACIENTE] {base_info}, RUT: {self._rut}, Tel: {self._telefono}"
    
    def to_dict(self):
        return {
            "id": self._id,
            "nombre": self._nombre,
            "rut": self._rut,
            "telefono": self._telefono
        }