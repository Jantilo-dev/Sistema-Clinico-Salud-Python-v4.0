import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from api.database.db import get_db_connection, close_connection

class UsuarioService:
    
    def registrar_usuario(self, nombre, correo, password):
        """Registra un nuevo usuario con la contraseña ENCRIPTADA"""
        conn = get_db_connection()
        if not conn: return False

        try:
            # Encriptamos la contraseña antes de guardar
            password_hash = generate_password_hash(password)
            
            cursor = conn.cursor()
            # CORREGIDO: Apuntando a JF_usuarios
            query = "INSERT INTO JF_usuarios (nombre, correo, password_hash) VALUES (%s, %s, %s)"
            cursor.execute(query, (nombre, correo, password_hash))
            conn.commit()
            print(f"Usuario {nombre} registrado correctamente.")
            return True

        except mysql.connector.IntegrityError:
            print("Error: El correo ya está registrado.")
            return False
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            return False
        finally:
            if cursor: cursor.close()
            close_connection(conn)

    def login(self, correo, password):
        """Valida correo y contraseña. Retorna True si es correcto."""
        conn = get_db_connection()
        if not conn: return False

        try:
            cursor = conn.cursor(dictionary=True)
            # CORREGIDO: Apuntando a JF_usuarios
            query = "SELECT password_hash, nombre FROM JF_usuarios WHERE correo = %s"
            cursor.execute(query, (correo,))
            usuario = cursor.fetchone()

            if usuario:
                # Verificamos si la contraseña coincide con el hash guardado
                if check_password_hash(usuario['password_hash'], password):
                    print(f"\n ¡Bienvenido/a, {usuario['nombre']}!")
                    return True
                else:
                    print(" Contraseña incorrecta.")
            else:
                print(" Usuario no encontrado.")
            
            return False

        except Exception as e:
            print(f" Error en login: {e}")
            return False
        finally:
            if cursor: cursor.close()
            close_connection(conn)
# ... (Mantén registrar y login) ...

    def listar_usuarios(self):
        conn = get_db_connection()
        if not conn: return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id_usuario, nombre, correo FROM JF_usuarios")
            return cursor.fetchall()
        except Exception as e:
            print(f" Error: {e}")
            return []
        finally:
            close_connection(conn)

    def eliminar_usuario(self, id_usuario):
        conn = get_db_connection()
        if not conn: return

        try:
            cursor = conn.cursor()
            query = "DELETE FROM JF_usuarios WHERE id_usuario = %s"
            cursor.execute(query, (id_usuario,))
            conn.commit()
            
            if cursor.rowcount > 0:
                print(f" Usuario ID {id_usuario} eliminado.")
            else:
                print(" Usuario no encontrado.")
        except Exception as e:
            print(f" Error: {e}")
        finally:
            close_connection(conn)