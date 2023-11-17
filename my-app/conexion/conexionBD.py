# Importando Libreria mysql.connector para conectar Python con MySQL
import mysql.connector

def connectionBD():
    try:
        # connection = mysql.connector.connect(
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="crud_python",
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
            port=3306  # Agregar el puerto 3306 aquí
        )

        if connection.is_connected():
            print("Conexión exitosa a la BD")
            return connection

    except mysql.connector.Error as error:
        print(f"No se pudo conectar: {error}")
        return None