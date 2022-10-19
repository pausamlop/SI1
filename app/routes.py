#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from email import message
import hashlib
from app import app
from flask import render_template, request, url_for, redirect, session, flash, Flask
import json
import os
import sys
import random
from pathlib import Path



@app.route('/')
@app.route('/principal', methods=['GET', 'POST'])
def principal():
    #print (url_for('static', filename='css/si1.css'), file=sys.stderr)
    catalogue_data = open(os.path.join(app.root_path,'catalogue/inventario.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    return render_template('principal.html', title = "Home", movies=catalogue['peliculas'])

@app.route('/frame')
def frame():
    #print (url_for('static', filename='css/si1.css'), file=sys.stderr)
    # print (url_for(filename='/templates/frame.html'), file=sys.stderr)
    return render_template('frame.html', title = "Home")


# VALORACION DE UNA PELICULA
@app.route('/valorar/<int:id>/<int:val>')
def valorar(id,val):
    catalogue_data = open(os.path.join(app.root_path,'catalogue/inventario.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    # encontrar peli a valorar
    for k in catalogue['peliculas']:
        if k["id"] == id:
            # encontrar antigua valoracion
            print('valoracion media:' + str(k["valoracion_media"]))
            # encontrar numero de usuarios que han votado
            print('numero valoraciones'+ str(k["numero_valoraciones"]))
            # calcular nueva media con la valoracion = (antigua*usuarios + nueva)/usuarios+1
            k['valoracion_media']= (float(k['valoracion_media'])*k["numero_valoraciones"]+val)/(k["numero_valoraciones"]+1)
            k['valoracion_media']="{0:.2f}".format(k['valoracion_media'])
            k["numero_valoraciones"]+=1

            # actualizar catalogue
            with open(os.path.join(app.root_path,'catalogue/inventario.json'), "w") as jf: 
                json.dump(catalogue, jf)

    print(id, val)
    return redirect(url_for('pelicula', id=id))



# PAGINA DE DETALLE DE LAS PELICULAS
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
        if (request.form['buscar'].lower() in k["titulo"].lower()) and (request.form['filtro'] in k["categoria"]):
            coincidencias.append(k)

    # redirigir a la pagina principal mostrando solo las coincidencias
    return render_template('principal.html', title = "Pelicula", movie_id=id, movies=coincidencias)




@app.route('/index')
def index():
    print (url_for('static', filename='css/si1.css'), file=sys.stderr)
    catalogue_data = open(os.path.join(app.root_path,'catalogue/inventario.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    return render_template('index.html', title = "Home", movies=catalogue['peliculas'])


@app.route('/showacceso', methods=['GET', 'POST'])
def showacceso():
    return render_template('acceso.html', title = "Acceso")

@app.route('/acceso', methods=['GET', 'POST'])
def acceso():

    usuario = request.form['username']
    pass1 = request.form['pass']

    app_folder = os.getcwd()
    path_user=os.path.join(app_folder, "si1users", usuario)

    #Comprobamos si el usuario existe
    if(os.path.isdir(path_user) == False):
        # flash("El usuario ya existe")
        error="El usuario no existe"
        return render_template('registro.html', error=error, title = "Registro")

    #Leemos la clave del dichero datos.dat del usuario
    path_datos=os.path.join(path_user, "datos.dat")
    dat = open(path_datos, 'r' ,encoding='utf-8')
    content = dat.readlines() 
    clave_dat=content[1]
    clave_dat=clave_dat[0:(len(clave_dat)-1)]
    dat.close()

    salt="superseguridadactivada"
    clave=hashlib.sha3_384((salt+pass1).encode('utf-8')).hexdigest()

    #Comparamos las claves
    if(clave_dat != clave):
        error="La clave no es corecta"
        return render_template('acceso.html', error=error, title = "Acceso")
    
    session['usuario']=usuario
    session['carrito']=list()
    session.modified=True

    return redirect(url_for('principal'))



@app.route('/showregistro', methods=['GET', 'POST'])
def showregistro():
    return render_template('registro.html', title = "Registro")

@app.route('/registro', methods=['GET', 'POST'])
def registro():

    usuario = request.form['username']
    email = request.form['email']
    tarjeta = request.form['tarjeta']
    direccion = request.form['direccion']
    pass1 = request.form['pass1']
    saldo = random.randint(0, 50)

    salt="superseguridadactivada"
    clave=hashlib.sha3_384((salt+pass1).encode('utf-8')).hexdigest()
    
    # Obtenemos el path a la carpeta usuario
    app_folder = os.getcwd()
    path_user=os.path.join(app_folder, "si1users", usuario)

    #Comprobamos si el usuario ya existe
    if(os.path.isdir(path_user)):
        # flash("El usuario ya existe")
        error="El usuario ya existe"
        return render_template('acceso.html', error=error, title = "Acceso")
    
    #Si no existe creamos la carpeta del usuario con los datos
    os.mkdir(path_user)
    path_datos=os.path.join(path_user, "datos.dat")
    path_compras=os.path.join(path_user, "compras.json")

    dat = open(path_datos, 'w' ,encoding='utf-8')
    dat.write(usuario + '\n')
    dat.write(clave)
    dat.write('\n'+ email + '\n')
    dat.write(tarjeta + '\n')
    dat.write(str(saldo) + '\n')
    dat.close()

    compras = open(path_compras, 'x' ,encoding='utf-8')
    compras.close()

    #Creamos la sesion del usuario
    session['usuario']=usuario
    session['carrito']=list()
    session.modified = True

    return redirect(url_for('principal'))


# PAGINA DEL CARRITO
@app.route('/carrito', methods=['GET', 'POST'])
def carrito():
    # cargar catalogo de peliculas
    catalogue_data = open(os.path.join(app.root_path,'catalogue/inventario.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    # buscar las que estan en el carrito
    carrito = list()
    for j in session['carrito']:
        for k in catalogue['peliculas']:
            if k["id"] == j:
                carrito.append(k)

    # redirigir a la pagina principal mostrando solo las coincidencias
    return render_template('carrito.html', title = "Pelicula", movies=carrito)


# ANADIR PELICULA AL CARRITO
@app.route('/anadircarrito/<int:id>')
def anadircarrito(id):
    # usuario anonimo
    if not session.get('carrito'):
        session['carrito']=list()
    # anadir pelicula
    session['carrito'].append(id)
    session.modified=True

    print(session['carrito'])

    return redirect('/principal')


# QUITAR PELICULA DEL CARRITO
@app.route('/eliminarcarrito/<int:id>')
def eliminarcarrito(id):
    # quitar pelicula
    session['carrito'].remove(id)
    session.modified=True
    return redirect('/carrito')



@app.route('/historialcompras', methods=['GET', 'POST'])
def historialcompras():
    return render_template('historialcompras.html', title = "Historial")

@app.route('/usu_conectados', methods=['GET', 'POST'])
def usu_conectados():
    return str(random.randint(1, 50))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('usuario', None)
    session.pop('carrito', None)
    session.modified = True
    return redirect(url_for('principal'))
