
# Para subir archivo tipo foto al servidor
from werkzeug.utils import secure_filename
import uuid  # Modulo de python para crear un string

from conexion.conexionBD import connectionBD  # Conexión a BD

import datetime
import re
import os

from os import remove  # Modulo  para remover archivo
from os import path  # Modulo para obtener la ruta o directorio


import openpyxl  # Para generar el excel
# biblioteca o modulo send_file para forzar la descarga
from flask import send_file


def procesar_form_producto(dataForm, foto_perfil):
    # Formateando Salario
    salario_sin_puntos = re.sub('[^0-9]+', '', dataForm['precio'])
    # convertir salario a INT
    salario_entero = int(salario_sin_puntos)

    result_foto_perfil = procesar_imagen_perfil(foto_perfil)

    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                sql = "INSERT INTO productos (nombre_producto, cantidad, descripcion_producto, foto_producto, precio) VALUES ( %s, %s, %s, %s, %s)"
                valores = (dataForm['nombre_producto'], dataForm['cantidad'], dataForm['descripcion_producto'], result_foto_perfil, salario_entero)
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                resultado_insert = cursor.rowcount
                return resultado_insert

    except Exception as e:
        return f'Se produjo un error en procesar_form_producto: {str(e)}'


def procesar_imagen_perfil(foto):
    try:
        # Nombre original del archivo
        filename = secure_filename(foto.filename)
        extension = os.path.splitext(filename)[1]

        # Creando un string de 50 caracteres
        nuevoNameFile = (uuid.uuid4().hex + uuid.uuid4().hex)[:100]
        nombreFile = nuevoNameFile + extension

        # Construir la ruta completa de subida del archivo
        basepath = os.path.abspath(os.path.dirname(__file__))
        upload_dir = os.path.join(basepath, f'../static/fotos_productos/')

        # Validar si existe la ruta y crearla si no existe
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
            # Dando permiso a la carpeta
            os.chmod(upload_dir, 0o755)

        # Construir la ruta completa de subida del archivo
        upload_path = os.path.join(upload_dir, nombreFile)
        foto.save(upload_path)

        return nombreFile

    except Exception as e:
        print("Error al procesar archivo:", e)
        return []


# Lista de productos
def sql_lista_productosBD():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    SELECT 
                        e.id_producto,
                        e.nombre_producto, 
                        e.cantidad,
                        e.precio,
                        e.foto_producto
                    FROM productos AS e
                    ORDER BY e.id_producto DESC
                """
                cursor.execute(querySQL,)
                productosBD = cursor.fetchall()

        return productosBD  # Devuelve la lista de productos

    except Exception as e:
        print(f"Error en la función sql_lista_productosBD: {e}")
        return None  # Devuelve None en caso de error

# Detalles del producto
def sql_detalles_productosBD(idproducto):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = ("""
                    SELECT 
                        e.id_producto,
                        e.nombre_producto, 
                        e.cantidad,
                        e.precio,
                        e.descripcion_producto,  # Corregir aquí, eliminar la coma al final
                        e.foto_producto
                    FROM productos AS e
                    WHERE id_producto = %s
                    ORDER BY e.id_producto DESC
                    """)
                cursor.execute(querySQL, (idproducto,))
                productosBD = cursor.fetchone()
        return productosBD
    except Exception as e:
        print(
            f"Errro en la función sql_detalles_productosBD: {e}")
        return None


# Funcion productos Informe (Reporte)
def productosReporte():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = ("""
                    SELECT 
                        e.id_producto,
                        e.nombre_producto, 
                        e.cantidad,
                        e.precio,
                        e.descripcion_producto,
                    FROM productos AS e
                    ORDER BY e.id_producto DESC
                    """)
                cursor.execute(querySQL,)
                productosBD = cursor.fetchall()
        return productosBD
    except Exception as e:
        print(
            f"Errro en la función productosReporte: {e}")
        return None



def buscarproductoBD(search):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                querySQL = ("""
                        SELECT 
                            e.id_producto,
                            e.nombre_producto, 
                            e.cantidad,
                            e.precio
                        FROM productos AS e
                        WHERE e.nombre_producto LIKE %s 
                        ORDER BY e.id_producto DESC
                    """)
                search_pattern = f"%{search}%"  # Agregar "%" alrededor del término de búsqueda
                mycursor.execute(querySQL, (search_pattern,))
                resultado_busqueda = mycursor.fetchall()
                return resultado_busqueda

    except Exception as e:
        print(f"Ocurrió un error en def buscarproductoBD: {e}")
        return []

def buscarproductoUnico(id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                querySQL = ("""
                        SELECT 
                            e.id_producto,
                            e.nombre_producto, 
                            e.cantidad,
                            e.descripcion_producto,
                            e.precio,
                            e.foto_producto
                        FROM productos AS e
                        WHERE e.id_producto =%s LIMIT 1
                    """)
                mycursor.execute(querySQL, (id,))
                producto = mycursor.fetchone()
                return producto

    except Exception as e:
        print(f"Ocurrió un error en def buscarproductoUnico: {e}")
        return []


def procesar_actualizacion_form(data):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                nombre_producto = data.form['nombre_producto']
                cantidad = data.form['cantidad']
                descripcion_producto = data.form['descripcion_producto']

                salario_sin_puntos = re.sub(
                    '[^0-9]+', '', data.form['precio'])
                precio = int(salario_sin_puntos)
                id_producto = data.form['id_producto']

                if data.files['foto_producto']:
                    file = data.files['foto_producto']
                    fotoForm = procesar_imagen_perfil(file)

                    querySQL = """
                        UPDATE productos
                        SET 
                            nombre_producto = %s,
                            cantidad = %s,
                            descripcion_producto = %s,
                            precio = %s,
                            foto_producto = %s
                        WHERE id_producto = %s
                    """
                    values = (nombre_producto, cantidad, descripcion_producto,
                              precio, fotoForm, id_producto)
                else:
                    querySQL = """
                        UPDATE productos
                        SET 
                            nombre_producto = %s,
                            cantidad = %s,
                            descripcion_producto = %s,
                            precio = %s
                        WHERE id_producto = %s
                    """
                    values = (nombre_producto, cantidad, descripcion_producto,
                              precio, id_producto)

                cursor.execute(querySQL, values)
                conexion_MySQLdb.commit()

        return cursor.rowcount or []
    except Exception as e:
        print(f"Ocurrió un error en procesar_actualizacion_form: {e}")
        return None


# Eliminar uproducto
def eliminarproducto(id_producto, foto_producto):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "DELETE FROM productos WHERE id_producto=%s"
                cursor.execute(querySQL, (id_producto,))
                conexion_MySQLdb.commit()
                resultado_eliminar = cursor.rowcount

                if resultado_eliminar:
                    # Eliminadon foto_producto desde el directorio
                    basepath = path.dirname(__file__)
                    url_File = path.join(
                        basepath, '../static/fotos_productos', foto_producto)

                    if path.exists(url_File):
                        remove(url_File)  # Borrar foto desde la carpeta

        return resultado_eliminar
    except Exception as e:
        print(f"Error en eliminarproducto : {e}")
        return []



def obtener_productos():
    try:
        connection = connectionBD()
        cursor = connection.cursor(dictionary=True)

        # Reemplaza 'nombre_de_tu_tabla' con el nombre real de la tabla
        cursor.execute("SELECT id_producto, nombre_producto, precio FROM productos")
        productos = cursor.fetchall()

        return productos
    except Exception as e:
        return str(e)
    finally:
        cursor.close()
        connection.close() 