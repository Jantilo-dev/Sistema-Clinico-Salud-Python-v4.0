# api/database/db.py
import mysql.connector
from mysql.connector import Error

#  INGRESA TUS CREDENCIALES AQUÍ
# Aca colocare un ejemplo de la conexión en MySQL. por motivos de privacidad no colocare las credenciales que ocupe para el proyecto
DB_CONFIG = {
            "host":"111.111.111.111",
            "port":3306,
            "user":"inacodec",
            "password":"1111111111111",
            "database":"inacodec"
}

def get_db_connection():
    """Establece y retorna la conexión a la base de datos MySQL"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f" Error crítico conectando a MySQL: {e}")
        return None

def close_connection(connection):
    """Cierra la conexión de forma segura"""
    if connection and connection.is_connected():
        connection.close()
