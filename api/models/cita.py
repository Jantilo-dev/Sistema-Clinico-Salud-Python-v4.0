# api/models/cita.py

class Cita:
    def __init__(self, id_cita, id_paciente, id_medico, fecha, hora, motivo, estado="Agendada"):
        self._id_cita = id_cita
        self._id_paciente = id_paciente
        self._id_medico = id_medico
        self._fecha = fecha
        self._hora = hora
        self._motivo = motivo
        self._estado = estado

    def mostrar_info(self):
        return f"Cita #{self._id_cita}: Paciente {self._id_paciente} con Médico {self._id_medico} el {self._fecha} a las {self._hora}"