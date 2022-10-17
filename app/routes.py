#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from flask import render_template, request, url_for, redirect, session
import json
import os
import sys
import random

@app.route('/')
@app.route('/principal', methods=['GET', 'POST'])
def principal():
    print ("buenas")
    print (url_for('static', filename='css/si1.css'), file=sys.stderr)
    catalogue_data = open(os.path.join(app.root_path,'catalogue/inventario.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    return render_template('principal.html', title = "Home", movies=catalogue['peliculas'])

@app.route('/frame')
def frame():
    print ("hola")
    print (url_for('static', filename='css/si1.css'), file=sys.stderr)
    # print (url_for(filename='/templates/frame.html'), file=sys.stderr)
    return render_template('frame.html', title = "Home")

@app.route('/pelicula/<int:id>')
def pelicula(id):
    catalogue_data = open(os.path.join(app.root_path,'catalogue/inventario.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    return render_template('pelicula.html', title = "Pelicula", movie_id=id, movies=catalogue['peliculas'])


# BUSQUEDA DE PELICULAS
@app.route('/busqueda', methods=['POST'])
def busqueda():
    # cargar catalogo de peliculas
    catalogue_data = open(os.path.join(app.root_path,'catalogue/inventario.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    # buscar en los catalogos y anadir las peliculas con coincidencias
    coincidencias = list()
    for k in catalogue['peliculas']:
        # busqueda y filtro
        if (request.form['buscar'] in k["titulo"]) and (request.form['filtro'] in k["categoria"]):
            coincidencias.append(k)

    # redirigir a la pagina principal mostrando solo las coincidencias
    return render_template('principal.html', title = "Pelicula", movie_id=id, movies=coincidencias)


@app.route('/index')
def index():
    print (url_for('static', filename='css/si1.css'), file=sys.stderr)
    catalogue_data = open(os.path.join(app.root_path,'catalogue/inventario.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    return render_template('index.html', title = "Home", movies=catalogue['peliculas'])

@app.route('/acceso', methods=['GET', 'POST'])
def acceso():

    
    # # doc sobre request object en http://flask.pocoo.org/docs/1.0/api/#incoming-request-data
    # if 'username' in request.form:
    #     # aqui se deberia validar con fichero .dat del usuario
    #     if request.form['username'] == 'pp':
    #         session['usuario'] = request.form['username']
    #         session.modified=True
    #         # se puede usar request.referrer para volver a la pagina desde la que se hizo login
    #         return redirect(url_for('principal'))
    #     else:
    #         # aqui se le puede pasar como argumento un mensaje de login invalido
    #         return render_template('registro.html', title = "Registro")
    # else:
    #     # se puede guardar la pagina desde la que se invoca 
    #     session['url_origen']=request.referrer
    #     session.modified=True        
    #     # print a error.log de Apache si se ejecuta bajo mod_wsgi
    #     print (request.referrer, file=sys.stderr)
    return render_template('acceso.html', title = "Acceso")



@app.route('/showregistro', methods=['GET', 'POST'])
def showregistro():
    return render_template('registro.html', title = "Registro")

@app.route('/registro', methods=['GET', 'POST'])
def registro():

    usuario = request.form['usuario']
    email = request.form['email']
    tarjeta = request.form['tarjeta']
    direccion = request.form['direccion']
    pass1 = request.form['pass1']
    saldo = random.randint(0, 50)
    
    
    
    return redirect(url_for('principal'))

    
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('usuario', None)
    return redirect(url_for('principal'))
