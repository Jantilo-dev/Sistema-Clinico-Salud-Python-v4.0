import mysql.connector
from api.database.db import get_db_connection, close_connection
from api.models.cita import Cita

class CitaService:
    
    def agendar_cita(self, cita: Cita):
        """
        Inserta una nueva cita en la BD.
        Maneja errores si el Paciente o Médico no existen.
        """
        conn = get_db_connection()
        if not conn: return

        try:
            cursor = conn.cursor()
            # Query para insertar en JF_Citas
            query = """
                INSERT INTO JF_Citas (id_paciente, id_medico, fecha, hora, motivo, estado) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            valores = (
                cita._id_paciente, # Accedemos a los atributos protegidos
                cita._id_medico, 
                cita._fecha, 
                cita._hora, 
                cita._motivo, 
                cita._estado
            )
            
            cursor.execute(query, valores)
            conn.commit()
            print(f" Cita agendada con éxito para la fecha {cita._fecha} a las {cita._hora}.")

        except mysql.connector.IntegrityError as e:
            # Este error salta si pones un ID de paciente/medico que no existe
            print(f" Error de Integridad: Es probable que el ID de Paciente o Médico no exista en la BD.\nDetalle: {e}")
        except mysql.connector.Error as e:
            print(f" Error al agendar cita: {e}")
        finally:
            if cursor: cursor.close()
            close_connection(conn)

    def listar_citas(self):
        """Devuelve una lista de objetos Cita"""
        conn = get_db_connection()
        lista_citas = []
        if not conn: return lista_citas

        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM JF_Citas"
            cursor.execute(query)
            resultados = cursor.fetchall()

            for fila in resultados:
                # Reconstruimos el objeto Cita
                cita = Cita(
                    id_cita=fila['id_cita'],
                    id_paciente=fila['id_paciente'],
                    id_medico=fila['id_medico'],
                    fecha=fila['fecha'],
                    hora=fila['hora'],
                    motivo=fila['motivo'],
                    estado=fila['estado']
                )
                lista_citas.append(cita)

        except mysql.connector.Error as e:
            print(f" Error al listar citas: {e}")
        finally:
            if cursor: cursor.close()
            close_connection(conn)
        
        return lista_citas

    def modificar_cita(self, id_cita, nueva_fecha, nueva_hora, nuevo_estado):
        """Actualiza fecha, hora o estado de una cita existente"""
        conn = get_db_connection()
        if not conn: return

        try:
            cursor = conn.cursor()
            query = """
                UPDATE JF_Citas 
                SET fecha = %s, hora = %s, estado = %s 
                WHERE id_cita = %s
            """
            valores = (nueva_fecha, nueva_hora, nuevo_estado, id_cita)
            cursor.execute(query, valores)
            conn.commit()
            
            if cursor.rowcount > 0:
                print(f" Cita #{id_cita} actualizada correctamente.")
            else:
                print(f" No se encontró la cita con ID {id_cita}.")

        except mysql.connector.Error as e:
            print(f" Error al actualizar: {e}")
        finally:
            if cursor: cursor.close()
            close_connection(conn)

    def eliminar_cita(self, id_cita):
        conn = get_db_connection()
        if not conn: return

        try:
            cursor = conn.cursor()
            query = "DELETE FROM JF_Citas WHERE id_cita = %s"
            cursor.execute(query, (id_cita,))
            conn.commit()

            if cursor.rowcount > 0:
                print(f" Cita #{id_cita} eliminada.")
            else:
                print(f" No se encontró la cita con ID {id_cita}.")

        except mysql.connector.Error as e:
            print(f" Error al eliminar: {e}")
        finally:
            if cursor: cursor.close()
            close_connection(conn)
    
    # BONUS: Método avanzado para listar con NOMBRES en vez de IDs (JOIN)
    # Esto no devuelve objetos Cita, sino un reporte legible para el usuario final.
    def obtener_reporte_citas(self):
        conn = get_db_connection()
        if not conn: return []
        
        reporte = []
        try:
            cursor = conn.cursor(dictionary=True)
            # Unimos las 3 tablas para ver nombres reales
            query = """
                SELECT c.id_cita, c.fecha, c.hora, c.estado, 
                       p.nombre as paciente, m.nombre as medico
                FROM JF_Citas c
                JOIN JF_Paciente p ON c.id_paciente = p.id_paciente
                JOIN JF_Medico m ON c.id_medico = m.id_medico
            """
            cursor.execute(query)
            reporte = cursor.fetchall()
        except mysql.connector.Error as e:
            print(f" Error generando reporte: {e}")
        finally:
            if cursor: cursor.close()
            close_connection(conn)
        return reporte