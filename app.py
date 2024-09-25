import pymongo
import pymongo.errors
import os
from flask import Flask, request, render_template, redirect, url_for


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/img'  
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  


miconexion = pymongo.MongoClient('mongodb://localhost:27017')
baseDatos = miconexion["Tienda2"]
productos = baseDatos["Productos1"]


@app.route("/")
def inicio():
    try:
        mensaje = None
        listarProductos = productos.find()
    except pymongo.errors.PyMongoError as error:
        mensaje = str(error)
    return render_template("inicio.html", productos=listarProductos, mensaje=mensaje)


@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        try:
            
            codigo = int(request.form['txtCodigo'])
            nombre = str(request.form['txtNombre'])
            precio = int(request.form['txtPrecio'])
            categoria = request.form['cbCategoria']
            foto = request.files['foto']

            
            if foto and foto.filename != '':
                foto_path = os.path.join(app.config['UPLOAD_FOLDER'], foto.filename)
                foto.save(foto_path)
            
           
            producto = {
                "codigo": codigo,
                "nombre": nombre,
                "precio": precio,
                "categoria": categoria,
                "foto": foto.filename if foto.filename != '' else None
            }

            
            productos.insert_one(producto)

           
            return redirect(url_for('inicio'))

        except pymongo.errors.PyMongoError as error:
            mensaje = str(error)
            return render_template("agregar.html", mensaje=mensaje)

    
    return render_template("agregar.html")


@app.route('/eliminar/<int:codigo>', methods=['POST'])
def eliminar(codigo):
    try:
        
        productos.delete_one({"codigo": codigo})

        
        return redirect(url_for('inicio'))

    except pymongo.errors.PyMongoError as error:
        mensaje = str(error)
        return render_template("inicio.html", mensaje=mensaje)
    
    
    
    
    
@app.route('/actualizar/<int:codigo>', methods=['GET', 'POST'])
def actualizar(codigo):
    try:
        producto = productos.find_one({"codigo": codigo})
        if request.method == 'POST':
            nombre = request.form['txtNombre']
            precio = int(request.form['txtPrecio'])
            categoria = request.form['cbCategoria']
            foto = request.files['foto']

            if foto and foto.filename != '':
                foto_path = os.path.join(app.config['UPLOAD_FOLDER'], foto.filename)
                foto.save(foto_path)

            productos.update_one({"codigo": codigo}, {"$set": {
                "nombre": nombre,
                "precio": precio,
                "categoria": categoria,
                "foto": foto.filename if foto.filename != '' else None
            }})

            
            listarProductos = productos.find()

            return redirect(url_for('inicio', productos=listarProductos))

        return render_template("actualizar.html", producto=producto)

    except pymongo.errors.PyMongoError as error:
        mensaje = str(error)
        return render_template("inicio.html", mensaje=mensaje)


@app.route('/listar', methods=['GET'])
def listar():
    try:
        productos_list = productos.find()
        return render_template("listar.html", productos=productos_list)

    except pymongo.errors.PyMongoError as error:
        mensaje = str(error)
        return render_template("inicio.html", mensaje=mensaje)
    
    

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])  
    app.run(port=3000, debug=True)
    
    




# Coleccion de Usuarios

# usuarios = baseDatos['Usuarios']

# Mostrar inormacion y luego valide para mostrar los productos


