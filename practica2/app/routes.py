#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from email import message
import hashlib
from app import app
from app import database
from flask import render_template, request, url_for, redirect, session, flash, Flask, make_response
import json
import os
import sys
import random
from pathlib import Path
from datetime import date


@app.route('/')
@app.route('/principal', methods=['GET', 'POST'])
def principal():

    return render_template('principal.html', title = "Home", movies = database.db_movieSelection(), 
                                topSales = database.db_topSales(), genres=database.db_getGenres())

@app.route('/frame')
def frame():
    return render_template('frame.html', title = "Home")


# VALORACION DE UNA PELICULA
@app.route('/valorar/<int:id>/<int:val>')
def valorar(id,val):

    # si el usuario no esta registrado, mandar al registro
    if not session.get('usuario'):
        return redirect(url_for('showregistroERR', error="Registrese antes de valorar una pelicula."))

    # WARNING HACE FALTA METER EL CUSTOMERID
    database.db_valorar(id, session['customerid'], val)

    print(id, val)

    return redirect(url_for('pelicula', id=id))



# PAGINA DE DETALLE DE LAS PELICULAS
@app.route('/pelicula/<int:id>')
def pelicula(id):

    d1 = database.db_movieData(id)
    d2 = database.db_getRatings(id)

    return render_template('pelicula.html', title = "Pelicula", prod_id=id, movies=d1, ratings=d2)



# BUSQUEDA DE PELICULAS
@app.route('/busqueda', methods=['POST'])
def busqueda():

    # busqueda en la base de datos
    coincidencias = database.db_searchFilterMovies(request.form['buscar'].lower(), request.form['filtro'])

    # get top sales
    topSales = database.db_topSales()
    # redirigir a la pagina principal mostrando solo las coincidencias
    return render_template('principal.html', title = "Pelicula", movie_id=id, 
            movies=coincidencias, topSales = topSales, genres=database.db_getGenres())




@app.route('/index')
def index():
    print (url_for('static', filename='css/si1.css'), file=sys.stderr)
    catalogue_data = open(os.path.join(app.root_path,'catalogue/inventario.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    return render_template('index.html', title = "Home", movies=catalogue['peliculas'])


@app.route('/showacceso', methods=['GET', 'POST'])
def showacceso():
    # si hay cookie
    cookie = request.cookies.get("usuario")
    if cookie == None:
        return render_template('acceso.html', title = "Acceso", cookie="")
    return render_template('acceso.html', title = "Acceso", user=cookie)

@app.route('/acceso', methods=['GET', 'POST'])
def acceso():

    usuario = request.form['username']
    pass1 = request.form['pass']

    
    #Comprobamos si el usuario existe
    if(database.db_user_exists(usuario) == False):
        error="El usuario no existe"
        return render_template('registro.html', error=error, title = "Registro")

 
    #Comparamos las claves
    ret = database.db_user_login(usuario, pass1)
    
    if( ret[0]== False):
        error="La clave no es corecta"
        # si hay cookie
        cookie = request.cookies.get("usuario")
        if cookie == None:
            return render_template('acceso.html', title = "Acceso", cookie="", error=error)
        return render_template('acceso.html', title = "Acceso", user=cookie, error=error)
    
    customerid = ret[1]

    session['customerid']=customerid
    session['usuario']=usuario
    session['carrito']=list()
    session.modified=True

    # guardar cookies
    cookie=make_response(redirect(url_for('principal')))
    cookie.set_cookie("usuario",usuario)

    return cookie


@app.route('/showregistro', methods=['GET', 'POST'])
def showregistro():
    return render_template('registro.html', title = "Registro")

@app.route('/showregistroERR/<string:error>', methods=['GET', 'POST'])
def showregistroERR(error):
    return render_template('registro.html', error=error, title = "Registro")

@app.route('/registro', methods=['GET', 'POST'])
def registro():

    usuario = request.form['username']
    email = request.form['email']
    tarjeta = request.form['tarjeta']
    direccion = request.form['direccion']
    pass1 = request.form['pass1']

    
    ret=database.db_user_register(direccion, email, tarjeta, usuario, pass1)

    #Si no existe lo añadimos a la base de datos
    if(ret[0] == True):
       
        #Creamos la sesion del usuario
        customerid = ret[1]

        session['customerid']=customerid
        session['usuario']=usuario
        session['carrito']=list()
        session.modified = True

        # guardar cookies
        cookie=make_response(redirect(url_for('principal')))
        cookie.set_cookie("usuario",usuario)

        return cookie

    elif(ret[0] == False):
        # flash("El usuario ya existe")
        error="El usuario ya existe"
        # si hay cookie
        cookie = request.cookies.get("usuario")
        if cookie == None:
            return render_template('acceso.html', title = "Acceso", cookie="", error=error)
        return render_template('acceso.html', title = "Acceso", user=cookie, error=error)
    

    return redirect(url_for('showregistroERR', error="Registro mal procesado por la base de datos"))



# PAGINA DEL CARRITO
@app.route('/carrito', methods=['GET', 'POST'])
def carrito():
    # cargar catalogo de peliculas
    catalogue_data = open(os.path.join(app.root_path,'catalogue/inventario.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    # buscar las que estan en el carrito
    carrito = list()
    total=0

    if not session.get('carrito'):
        session['carrito']=[]
        session.modified=True

    for j in session['carrito']:
        for k in catalogue['peliculas']:
            if k["id"] == j:
                carrito.append(k)
                total+=k["precio"]

    # diccionario con el id y la cantidad en el carrito
    carrito_dict = dict()
    for k in carrito:
        if not carrito_dict.get(k["id"]):
            carrito_dict[k["id"]] = 1
        else:
            carrito_dict[k["id"]] += 1

    # redirigir a la pagina principal mostrando solo las coincidencias
    return render_template('carrito.html', title = "Pelicula", movies=catalogue['peliculas'], total="{0:.2f}".format(total), carrito_dict=carrito_dict)


# ANADIR PELICULA AL CARRITO
@app.route('/anadircarrito/<int:id>/<int:next>')
def anadircarrito(id, next):
    # usuario anonimo
    if not session.get('carrito'):
        session['carrito']=list()
    # anadir pelicula
    session['carrito'].append(id)
    session.modified=True
    # aumentada la cantidad desde la pagina de detalle
    if next == 0:
        return redirect('/principal')
    #aumentada la cantidad desde el carrito
    return redirect('/carrito')


# QUITAR PELICULA DEL CARRITO
@app.route('/eliminarcarrito/<int:id>')
def eliminarcarrito(id):
    # quitar pelicula
    session['carrito'].remove(id)
    session.modified=True
    return redirect('/carrito')


# PAGAR 
@app.route('/pagar/<float:total>') 
def pagar(total):
    # si el usuario no esta registrado, ir al registro
    if not session.get('usuario'):
        return render_template('registro.html', error="Registrese antes de finalizar su compra", title = "Registro") 
    # leer el archivo
    datos = open(os.path.join(app.root_path,"../si1users/"+session['usuario']+"/datos.dat"), encoding="utf-8").readlines()
    # comprobar saldo
    saldo = float(datos[4])
    # si no hay saldo suficiente volver al carrito
    if saldo < total:
        catalogue_data = open(os.path.join(app.root_path,'catalogue/inventario.json'), encoding="utf-8").read()
        catalogue = json.loads(catalogue_data)

        return render_template('principal.html', title = "Home", movies = database.db_movieSelection(),
                                    topSales = database.db_topSales(), genres=database.db_getGenres())
    
    # actualizar saldo
    datos[4]=str(saldo-total)
    datos_string= datos[0]+datos[1]+datos[2]+datos[3]+datos[4]
    open(os.path.join(app.root_path,"../si1users/"+session['usuario']+"/datos.dat"),"w").write(datos_string)
    
    # anadir a compras.json
    catalogue_data = open(os.path.join(app.root_path,'catalogue/inventario.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    c_data = open(os.path.join(app.root_path,"../si1users/"+session['usuario']+"/compras.json"), encoding="utf-8").read()

    if not c_data:
        c = {'peliculas':[]}
    else:
        c = json.loads(c_data)
    
    if not c['peliculas']:
        c['peliculas'] = []

    for k in session['carrito']:
        for j in catalogue['peliculas']:
            if k == j['id']:
                j['fecha']=str(date.today())
                c['peliculas'].append(j)
               
    json.dump(c, open(os.path.join(app.root_path,"../si1users/"+session['usuario']+"/compras.json"), "w"))

    # vaciar el carrito
    session['carrito']=[]
    session.modified = True
    # get top sales
    topSales = database.db_topSales()
    return render_template('principal.html', total=total, error="Compra procesada correctamente",
            movies=database.db_movieSelection(),title = "Home", topSales = topSales, genres=database.db_getGenres())



@app.route('/historialcompras', methods=['GET', 'POST'])
def historialcompras():
    if 'usuario' not in session:
        error="Por favor, primero inicie sesión"
        # si hay cookie
        cookie = request.cookies.get("usuario")
        if cookie == None:
            return render_template('acceso.html', title = "Acceso", cookie="", error=error)
        return render_template('acceso.html', title = "Acceso", user=cookie, error=error)
        
    
    
    customerid=session['customerid']

    
    saldo = database.db_get_saldo(customerid)
    compras_cliente = database.db_historial(customerid)

    return render_template('historialcompras.html', title = "Historial", compras=compras_cliente, saldo=saldo)



@app.route('/aumento_saldo', methods=['POST'])
def aumento_saldo():

    aumento_saldo = request.form['aumento_saldo']
    customerid=session['customerid']

    database.db_increase_saldo(customerid, aumento_saldo)

    return redirect(url_for('historialcompras'))



@app.route('/usu_conectados', methods=['GET', 'POST'])
def usu_conectados():
    return str(random.randint(1, 50))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('customerid', None)
    session.pop('usuario', None)
    session.pop('carrito', None)
    session.modified = True
    return redirect(url_for('principal'))
