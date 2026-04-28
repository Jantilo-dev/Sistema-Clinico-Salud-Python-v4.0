# api/database/db.py
import mysql.connector
from mysql.connector import Error

#  INGRESA TUS CREDENCIALES AQUÍ
DB_CONFIG = {
            "host":"138.255.103.114",
            "port":3306,
            "user":"inacodec_poo_seccion_c2",
            "password":"AQm}ZzpW0ovqyaZJ",
            "database":"inacodec_dataPracticaApis" # Asegúrate de poner el nombre real de la BD
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