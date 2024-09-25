from app import app, usuarios
from flask import render_template, request, redirect

@app.route("/", methods=['GET', 'POST'])
def loading():
    if  request.method == 'GET':
        return render_template('frmLoding.html')
    else
    username = request.from['txtUsername']
    passaword = request.from['txtPassaword']
    usuario = {
        "username":username,
        "passaword":passaword
    }
userExiste = usuario.find_one(usuario)
if(userExiste):
    redirect(/listarProductos)
    