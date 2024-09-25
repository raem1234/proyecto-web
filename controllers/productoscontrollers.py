from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.security import check_password_hash
import pymongo
import pymongo.errors
import os
import yagmail


app = Flask(__name__)
app.secret_key = '123456789'  
app.config['UPLOAD_FOLDER'] = './static/img'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


miconexion = pymongo.MongoClient('mongodb://localhost:27017')
baseDatos = miconexion["Tienda"]
usuarios = baseDatos["Usuarios"]
productos = baseDatos["Productos"]

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['txtUsername']
        password = request.form['txtPassword']

        
        usuario = usuarios.find_one({"nombre_usuario": username})
        
        if usuario and check_password_hash(usuario['contraseña'], password):
            session['user'] = username
            return redirect(url_for('listar_productos'))
        else:
            mensaje = "Credenciales de Ingreso No Válidas"
            return render_template('formLogin.html', mensaje=mensaje)
    
    return render_template('formLogin.html')

@app.route('/salir')
def salir():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/listar_productos')
def listar_productos():
    if 'user' not in session:
        return redirect(url_for('login'))

    try:
        listarProductos = productos.find()
        return render_template('listarProductos.html', productos=listarProductos)
    except pymongo.errors.PyMongoError as error:
        mensaje = str(error)
        return render_template('listarProductos.html', mensaje=mensaje)

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(port=3000, debug=True)
     