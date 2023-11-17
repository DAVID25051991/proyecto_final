from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify
from mysql.connector.errors import Error


# Importando cenexión a BD
from controllers.funciones_productos import *

PATH_URL = "public/productos"


@app.route('/registrar-producto', methods=['GET'])
def viewFormproducto():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/form_productos.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/form-registrar-producto', methods=['POST'])
def formproducto():
    if 'conectado' in session:
        if 'foto_producto' in request.files:
            foto_perfil = request.files['foto_producto']
            resultado = procesar_form_producto(request.form, foto_perfil)
            if resultado:
                return redirect(url_for('lista_productos'))
            else:
                flash('El producto NO fue registrado.', 'error')
                return render_template(f'{PATH_URL}/form_productos.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/lista-de-productos', methods=['GET'])
def lista_productos():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/lista_productos.html', productos=sql_lista_productosBD())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route("/detalles-producto/", methods=['GET'])
@app.route("/detalles-producto/<int:idproducto>", methods=['GET'])
def detalleproducto(idproducto=None):
    if 'conectado' in session:
        # Verificamos si el parámetro idproducto es None o no está presente en la URL
        if idproducto is None:
            return redirect(url_for('inicio'))
        else:
            detalle_producto = sql_detalles_productosBD(idproducto) or []
            return render_template(f'{PATH_URL}/detalles_productos.html', detalle_producto=detalle_producto)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Buscadon de productos
@app.route("/buscando-producto", methods=['POST'])
def viewBuscarproductoBD():
    resultadoBusqueda2 = buscarproductoBD(request.json['busqueda2'])
    if resultadoBusqueda2:
        return render_template(f'{PATH_URL}/resultado_busqueda_productos.html', dataBusqueda2=resultadoBusqueda2)
    else:
        return jsonify({'fin': 0})


@app.route("/editar-producto/<int:id>", methods=['GET'])
def viewEditarproducto(id):
    if 'conectado' in session:
        respuestaproducto = buscarproductoUnico(id)
        if respuestaproducto:
            return render_template(f'{PATH_URL}/form_productos_update.html', respuestaproducto=respuestaproducto)
        else:
            flash('El producto no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Recibir formulario para actualizar información de producto
@app.route('/actualizar-producto', methods=['POST'])
def actualizarproducto():
    resultData = procesar_actualizacion_form(request)
    if resultData:
        flash('producto actualizado correctamente', 'success')
        return redirect(url_for('lista_productos'))
    else:
        flash('Error al actualizar producto', 'error')
        return render_template('error.html')

@app.route('/borrar-producto/<string:id_producto>/<string:foto_producto>', methods=['GET'])
def borrarproducto(id_producto, foto_producto):
    resp = eliminarproducto(id_producto, foto_producto)
    if resp:
        flash('El producto fue eliminado correctamente', 'success')
        return redirect(url_for('lista_productos'))


@app.route('/registrar-producto')
def registrar_producto():
    return render_template('form_productos.html')


@app.route('/caja', methods=['GET'])
def viewFormcaja():
    if 'conectado' in session:
        productos = obtener_productos()
        return render_template(f'{PATH_URL}/caja_registradora.html',productos=productos)
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
