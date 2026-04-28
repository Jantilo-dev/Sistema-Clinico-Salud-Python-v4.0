# api/services/medico_service.py
import mysql.connector
from api.database.db import get_db_connection, close_connection
from api.models.medico import Medico

class MedicoService:
    def crear_medico(self, medico: Medico):
        conn = get_db_connection()
        if not conn: return

        try:
            cursor = conn.cursor()
            query = "INSERT INTO JF_Medico (nombre, especialidad) VALUES (%s, %s)"
            cursor.execute(query, (medico.nombre, medico.especialidad))
            conn.commit()
            print(" Médico registrado.")
        except mysql.connector.Error as e:
            print(f" Error BD: {e}")
        finally:
            if cursor: cursor.close()
            close_connection(conn)

    def listar_medicos(self):
        conn = get_db_connection()
        lista = []
        if not conn: return lista

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM JF_Medico")
            for fila in cursor.fetchall():
                # Instanciamos la clase Medico
                lista.append(Medico(fila['id_medico'], fila['nombre'], fila['especialidad']))
        except Exception as e:
            print(f" Error: {e}")
        finally:
            close_connection(conn)
        return lista
    
# ... (Mantén los métodos anteriores) ...

    def eliminar_medico(self, id_medico):
        conn = get_db_connection()
        if not conn: return

        try:
            cursor = conn.cursor()
            
            # PASO 1: Borrar citas asociadas a este médico
            cursor.execute("DELETE FROM JF_Citas WHERE id_medico = %s", (id_medico,))
            
            # PASO 2: Borrar médico
            query = "DELETE FROM JF_Medico WHERE id_medico = %s"
            cursor.execute(query, (id_medico,))
            conn.commit()

            if cursor.rowcount > 0:
                print(f" Médico ID {id_medico} eliminado.")
            else:
                print(f" No se encontró médico con ID {id_medico}.")

        except mysql.connector.Error as e:
            print(f" Error al eliminar: {e}")
        finally:
            if cursor: cursor.close()
            close_connection(conn)