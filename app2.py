# --------------------------------------------------------------------

# Instalar con pip install Flask
from flask import Flask, request, jsonify, render_template
from flask import request

# Instalar con pip install flask-cors
from flask_cors import CORS

# Instalar con pip install mysql-connector-python
import mysql.connector

# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename

# No es necesario instalar, es parte del sistema standard de Python
import os
import time

app = Flask(__name__)
CORS(app)  # Esto habilitará CORS para todas las rutas

# --------------------------------------------------------------------


class Catalogo:
    # ----------------------------------------------------------------
    # Constructor de la clase
    def __init__(self, host, user, password, database):
        # Primero, establecemos una conexión sin especificar la base de datos
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()

        # Intentamos seleccionar la base de datos
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            # Si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        # Una vez que la base de datos está establecida, creamos la tabla si no existe
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS autos (
            codigo INT AUTO_INCREMENT PRIMARY KEY,
            color VARCHAR(50) NOT NULL,
            modelo VARCHAR(15) NOT NULL,
            marca VARCHAR(50) NOT NULL,                 
            cantidad INT NOT NULL,
            precio DECIMAL(10, 2) NOT NULL,
            imagen_url VARCHAR(255))''')
        self.conn.commit()

        # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)

    # ---------------------------------------------------------------- HECHO: NO TOCAR
    def agregar_auto(self, color, modelo, marca, cantidad, precio, imagen):

        sql = "INSERT INTO autos (color, modelo, marca, cantidad, precio, imagen_url) VALUES (%s, %s, %s, %s, %s, %s)"
        valores = (color, modelo, marca, cantidad, precio, imagen)

        self.cursor.execute(sql, valores)
        self.conn.commit()
        # esto devuelve el ultimo ID insertado
        return self.cursor.lastrowid

    # ---------------------------------------------------------------- NO TOCAR
    def consultar_auto(self, codigo):
        # Consultamos un Auto a partir de su código
        self.cursor.execute(f"SELECT * FROM autos WHERE codigo = {codigo}")
        return self.cursor.fetchone()

    # ------------- MODIFICADO POR PAMELA ---------------------------------------
    def modificar_auto(self, codigo, nuevo_color, nuevo_modelo, nueva_marca, nueva_cantidad, nuevo_precio, nueva_imagen):
        sql = "UPDATE autos SET color = %s, modelo = %s, marca = %s, cantidad = %s, precio = %s, imagen_url = %s WHERE codigo = %s"
        valores = (nuevo_color, nuevo_modelo, nueva_marca,
                   nueva_cantidad, nuevo_precio, nueva_imagen, codigo)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

    # ---------------------------------------------------------------- HECHO
    def listar_autos(self):
        self.cursor.execute("SELECT * FROM autos")
        autos = self.cursor.fetchall()
        return autos

    # ---------------------------------------------------------------- HECHO
    # ------------- MODIFICADO POR PAMELA ---------------------------------------
    def eliminar_auto(self, codigo):
        # Eliminamos un Auto de la tabla a partir de su código
        self.cursor.execute(f"DELETE FROM autos WHERE codigo = {codigo}")
        self.conn.commit()
        return self.cursor.rowcount > 0

    # ---------------------------------------------------------------- HECHO
    def mostrar_auto(self, codigo):
        # Mostramos los datos de un Auto a partir de su código
        Auto = self.consultar_auto(codigo)
        if Auto:
            print("-" * 40)
            print(f"Código.....: {Auto['codigo']}")
            print(f"color: {Auto['color']}")
            print(f"modelo: {Auto['modelo']}")
            print(f"marca: {Auto['marca']}")
            print(f"Cantidad...: {Auto['cantidad']}")
            print(f"Precio.....: {Auto['precio']}")
            print(f"Imagen.....: {Auto['imagen_url']}")
            # print(f"Proveedor..: {Auto['proveedor']}")
            print("-" * 40)
        else:
            print("Auto no encontrado o inexistente.")


# --------------------------------------------------------------------
# Cuerpo del programa
# --------------------------------------------------------------------
# Crear una instancia de la clase Catalogo

# catalogo = Catalogo(host='localhost', user='root',
#                     password='', database='mi_app')


# catalogo = Catalogo(host='localhost', user='root',
#                     password='root', database='miapp')
# catalogo = Catalogo(host='USUARIO.mysql.pythonanywhere-services.com', user='USUARIO', password='CLAVE', database='USUARIO$miapp')
catalogo = Catalogo(host='gaston2024.mysql.pythonanywhere-services.com', user='gaston2024', password='33723372abc', database='gaston2024$miapp')


# Carpeta para guardar las imagenes.
# RUTA_DESTINO = './static/imagenes/'
# RUTA_DESTINO = os.path.join(os.path.dirname(__file__), '..', 'static', 'imagenes','/')
# if not os.path.exists(RUTA_DESTINO):
#     os.makedirs(RUTA_DESTINO)


# Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
# RUTA_DESTINO = '/home/USUARIO/mysite/static/imagenes'
RUTA_DESTINO = '/home/gaston2024/mysite/static/imagenes'


# --------------------------------------------------------------------
# Listar todos los Autos
# --------------------------------------------------------------------
# La ruta Flask /Autos con el método HTTP GET está diseñada para proporcionar los detalles de todos los Autos almacenados en la base de datos.
# El método devuelve una lista con todos los Autos en formato JSON.

# -------------------------------------- HECHO: NO TOCAR
@app.route("/autos", methods=["GET"])
def listar_autos():
    autos = catalogo.listar_autos()
    return jsonify(autos)


# --------------------------------------------------------------------
# Mostrar un sólo Auto según su código
# --------------------------------------------------------------------
# La ruta Flask /Autos/<int:codigo> con el método HTTP GET está diseñada para proporcionar los detalles de un Auto específico basado en su código.
# El método busca en la base de datos el Auto con el código especificado y devuelve un JSON con los detalles del Auto si lo encuentra, o None si no lo encuentra.

# --------------------------------------------------- HECHO: NO TOCAR
@app.route("/autos/<int:codigo>", methods=["GET"])
def mostrar_auto(codigo):
    # esta funcion hace uso de la funcion anterior de arriba para consultar mediante codigo
    auto = catalogo.consultar_auto(codigo)
    if auto:
        return jsonify(auto), 201
    else:
        return "Auto no encontrado", 404


# --------------------------------------------------------------------
# Agregar un Auto
# --------------------------------------------------------------------
@app.route("/autos", methods=["POST"])
# La ruta Flask `/Autos` con el método HTTP POST está diseñada para permitir la adición de un nuevo Auto a la base de datos.
# La función agregar_Auto se asocia con esta URL y es llamada cuando se hace una solicitud POST a /Autos.
def agregar_auto():
    
    # Recojo los datos del form
    color = request.form['color']
    modelo = request.form['modelo']
    marca = request.form['marca']
    cantidad = request.form['cantidad']
    precio = request.form['precio']
    imagen = request.files['imagen']
    nombre_imagen = ""

    # Genero el nombre de la imagen
    # Chequea el nombre del archivo de la imagen, asegurándose de que sea seguro para guardar en el sistema de archivos
    nombre_imagen = secure_filename(imagen.filename)
    # Separa el nombre del archivo de su extensión.
    nombre_base, extension = os.path.splitext(nombre_imagen)
    # Genera un nuevo nombre para la imagen usando un timestamp, para evitar sobreescrituras y conflictos de nombres.
    nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"

    nuevo_codigo = catalogo.agregar_auto(
        color, modelo, marca, cantidad, precio, nombre_imagen)
    if nuevo_codigo:
        imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))

        # Si el Auto se agrega con éxito, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 201 (Creado).
        return jsonify({"mensaje": "Auto agregado correctamente.", "codigo": nuevo_codigo, "imagen": nombre_imagen}), 201
    else:
        # Si el Auto no se puede agregar, se devuelve una respuesta JSON con un mensaje de error y un código de estado HTTP 500 (Internal Server Error).
        return jsonify({"mensaje": "Error al agregar el auto."}), 500

    # try:
    #     nuevo_codigo = catalogo.agregar_auto(color, modelo, marca, cantidad, precio, nombre_imagen)
    #     imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))
    #     return jsonify({"mensaje": "Auto agregado correctamente.", "codigo": nuevo_codigo, "imagen": nombre_imagen}), 201
    # except Exception as e:
    #     return jsonify({"mensaje": f"Error al agregar el auto: {str(e)}"}), 500


# --------------------------------------------------------------------
# Modificar un Auto según su código
# --------------------------------------------------------------------

@app.route("/autos/<int:codigo>", methods=["PUT"])
# La ruta Flask /Autos/<int:codigo> con el método HTTP PUT está diseñada para actualizar la información de un Auto existente en la base de datos, identificado por su código.
# La función modificar_Auto se asocia con esta URL y es invocada cuando se realiza una solicitud PUT a /Autos/ seguido de un número (el código del Auto).
def modificar_auto(codigo):
    # Se recuperan los nuevos datos del formulario
    nuevo_color = request.form.get("color")
    nuevo_modelo = request.form.get("modelo")
    nueva_marca = request.form.get("marca")
    nueva_cantidad = request.form.get("cantidad")
    nuevo_precio = request.form.get("precio")

    # Verifica si se proporcionó una nueva imagen
    if 'imagen' in request.files:
        imagen = request.files['imagen']
        # Procesamiento de la imagen
        # Chequea el nombre del archivo de la imagen, asegurándose de que sea seguro para guardar en el sistema de archivos
        nombre_imagen = secure_filename(imagen.filename)
        # Separa el nombre del archivo de su extensión.
        nombre_base, extension = os.path.splitext(nombre_imagen)
        # Genera un nuevo nombre para la imagen usando un timestamp, para evitar sobreescrituras y conflictos de nombres.
        nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"

        # Guardar la imagen en el servidor
        imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))

        # Busco el Auto guardado
        Auto = catalogo.consultar_auto(codigo)
        if Auto:  # Si existe el Auto...
            imagen_vieja = Auto["imagen_url"]
            # Armo la ruta a la imagen
            ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

            # Y si existe la borro.
            if os.path.exists(ruta_imagen):
                os.remove(ruta_imagen)

    else:
        # Si no se proporciona una nueva imagen, simplemente usa la imagen existente del Auto
        Auto = catalogo.consultar_auto(codigo)
        if Auto:
            nombre_imagen = Auto["imagen_url"]

    # Se llama al método modificar_Auto pasando el codigo del Auto y los nuevos datos.
    if catalogo.modificar_auto(codigo, nuevo_color, nuevo_modelo, nueva_marca, nueva_cantidad, nuevo_precio, nombre_imagen):

        # Si la actualización es exitosa, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 200 (OK).
        return jsonify({"mensaje": "Auto modificado"}), 200
    else:
        # Si el Auto no se encuentra (por ejemplo, si no hay ningún Auto con el código dado), se devuelve un mensaje de error con un código de estado HTTP 404 (No Encontrado).
        return jsonify({"mensaje": "Auto no encontrado"}), 403


# --------------------------------------------------------------------
# Eliminar un Auto según su código
# --------------------------------------------------------------------

@app.route("/autos/<int:codigo>", methods=["DELETE"])
# La ruta Flask /Autos/<int:codigo> con el método HTTP DELETE está diseñada para eliminar un Auto específico de la base de datos, utilizando su código como identificador.
# La función eliminar_Auto se asocia con esta URL y es llamada cuando se realiza una solicitud DELETE a /Autos/ seguido de un número (el código del Auto).
def eliminar_auto(codigo):
    # Busco el Auto en la base de datos
    Auto = catalogo.consultar_auto(codigo)
    if Auto:  # Si el Auto existe, verifica si hay una imagen asociada en el servidor.
        imagen_vieja = Auto["imagen_url"]
        # Armo la ruta a la imagen
        ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

        # Y si existe, la elimina del sistema de archivos.
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)

        # Luego, elimina el Auto del catálogo
        if catalogo.eliminar_auto(codigo):
            # Si el Auto se elimina correctamente, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 200 (OK).
            return jsonify({"mensaje": "Auto eliminado"}), 200
        else:
            # Si ocurre un error durante la eliminación (por ejemplo, si el Auto no se puede eliminar de la base de datos por alguna razón), se devuelve un mensaje de error con un código de estado HTTP 500 (Error Interno del Servidor).
            return jsonify({"mensaje": "Error al eliminar el auto"}), 500
    else:
        # Si el Auto no se encuentra (por ejemplo, si no existe un Auto con el codigo proporcionado), se devuelve un mensaje de error con un código de estado HTTP 404 (No Encontrado).
        return jsonify({"mensaje": "Auto no encontrado"}), 404


# --------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
