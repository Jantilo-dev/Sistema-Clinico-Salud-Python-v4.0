# api/services/paciente_service.py
import mysql.connector
from api.database.db import get_db_connection, close_connection
from api.models.paciente import Paciente

class PacienteService:
    
    def crear_paciente(self, paciente: Paciente):
        conn = get_db_connection()
        if not conn:
            print(" No hay conexión a la base de datos.")
            return

        try:
            cursor = conn.cursor()
            # Query segura con placeholders %s
            query = "INSERT INTO JF_Paciente (nombre, rut, telefono) VALUES (%s, %s, %s)"
            # Obtenemos los datos del objeto (Encapsulamiento)
            valores = (paciente.nombre, paciente.rut, paciente.telefono)
            
            cursor.execute(query, valores)
            conn.commit()
            print(f" Paciente {paciente.nombre} registrado con éxito.")
            
        except mysql.connector.IntegrityError as e:
            # Manejo de error de claves duplicadas (Requisito 2.1.5)
            print(f" Error: Ya existe un paciente con esos datos (Posible RUT duplicado). Detalle: {e}")
        except mysql.connector.Error as e:
            print(f" Error de base de datos: {e}")
        finally:
            if cursor: cursor.close()
            close_connection(conn)

    def listar_pacientes(self):
        conn = get_db_connection()
        lista_pacientes = []
        if not conn: return lista_pacientes

        try:
            cursor = conn.cursor(dictionary=True) # Para acceder por nombre de columna
            query = "SELECT * FROM JF_Paciente"
            cursor.execute(query)
            resultados = cursor.fetchall()

            for fila in resultados:
                # Convertimos el diccionario de la BD a un objeto Paciente
                # Asumiendo que tu tabla tiene id_paciente, nombre, rut, telefono
                nuevo_paciente = Paciente(
                    id_paciente=fila['id_paciente'], 
                    nombre=fila['nombre'], 
                    rut=fila['rut'], 
                    telefono=fila['telefono']
                )
                lista_pacientes.append(nuevo_paciente)

        except mysql.connector.Error as e:
            print(f" Error al listar: {e}")
        finally:
            if cursor: cursor.close()
            close_connection(conn)
        
        return lista_pacientes

    def buscar_por_rut(self, rut):
        conn = get_db_connection()
        if not conn: return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM JF_Paciente WHERE rut = %s"
            cursor.execute(query, (rut,))
            fila = cursor.fetchone()

            if fila:
                return Paciente(fila['id_paciente'], fila['nombre'], fila['rut'], fila['telefono'])
            else:
                return None
        except mysql.connector.Error as e:
            print(f" Error en búsqueda: {e}")
            return None
        finally:
            if cursor: cursor.close()
            close_connection(conn)
            
# ... (Mantén los métodos anteriores crear y listar) ...

    def eliminar_paciente(self, id_paciente):
        conn = get_db_connection()
        if not conn: return

        try:
            cursor = conn.cursor()
            
            # PASO 1: Borrar el historial de citas de este paciente (para evitar error FK)
            cursor.execute("DELETE FROM JF_Citas WHERE id_paciente = %s", (id_paciente,))
            
            # PASO 2: Ahora sí, borrar al paciente
            query = "DELETE FROM JF_Paciente WHERE id_paciente = %s"
            cursor.execute(query, (id_paciente,))
            conn.commit()

            if cursor.rowcount > 0:
                print(f" Paciente ID {id_paciente} y su historial fueron eliminados.")
            else:
                print(f" No se encontró paciente con ID {id_paciente}.")

        except mysql.connector.Error as e:
            print(f" Error al eliminar: {e}")
        finally:
            if cursor: cursor.close()
            close_connection(conn)