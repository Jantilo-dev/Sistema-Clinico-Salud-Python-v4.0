# api/models/persona.py
class Persona:
    def __init__(self, id_persona, nombre):
        self._id = id_persona      # Encapsulamiento (protegido)
        self._nombre = nombre      # Encapsulamiento

    # Getters y Setters
    @property
    def id(self):
        return self._id
    
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor

    # Método para Polimorfismo
    def mostrar_info(self):
        return f"ID: {self._id}, Nombre: {self._nombre}"