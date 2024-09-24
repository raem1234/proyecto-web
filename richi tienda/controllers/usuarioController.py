from app import app, usuarios
from flask import render_template, request, redirect, session
import yagmail
import threading


@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['txtUsername']
        password = request.form['txtPassword']
        usuario = {"username": username, "password": password}

        if usuarios.find_one(usuario):
            session['user'] = usuario
            email = yagmail.SMTP("ricardoandreserazomunoz@gmail.com", open(".password").read(), encoding='UTF-8')
            mensaje = f"el usuario {username} ha ingresado al sistema"
            thread = threading.Thread(target=enviarCorreo, args=(email, "ricardoandreserazomunoz@gmail.com", "Reporte ingreso al sistema usuario", mensaje))
            thread.start()
            return redirect("/listarProductos")
        
        return render_template("formLogin.html", mensaje="Credencialesno válidas")
    
    return render_template("formLogin.html")


@app.route("/salir")
def salir():
    session.clear()  
    return render_template("formLogin.html", mensaje=" cerrado la sesión.")


def enviarCorreo(email, destinatario, asunto, mensaje):
    email.send(to=destinatario, subject=asunto, contents=mensaje)
