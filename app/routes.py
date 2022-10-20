#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from email import message
import hashlib
from app import app
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
    catalogue_data = open(os.path.join(app.root_path,'catalogue/inventario.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    return render_template('principal.html', title = "Home", movies=catalogue['peliculas'])

@app.route('/frame')
def frame():
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
    # si hay cookie
    cookie = request.cookies.get("usuario")
    if cookie == None:
        return render_template('acceso.html', title = "Acceso", cookie="")
    return render_template('acceso.html', title = "Acceso", user=cookie)

@app.route('/acceso', methods=['GET', 'POST'])
def acceso():

    usuario = request.form['username']
    pass1 = request.form['pass']

    app_folder = os.getcwd()
    path_user=os.path.join(app_folder, "si1users", usuario)

    #Comprobamos si el usuario existe
    if(os.path.isdir(path_user) == False):
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
            # si hay cookie
        cookie = request.cookies.get("usuario")
        if cookie == None:
            return render_template('acceso.html', title = "Acceso", cookie="", error=error)
        return render_template('acceso.html', title = "Acceso", user=cookie,error=error)
    
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
    path_folder_users=os.path.join(app_folder, "si1users")
    

    if(os.path.isdir(path_folder_users) == False):
        os.mkdir(path_folder_users)

    path_user=os.path.join(app_folder, "si1users", usuario)

    #Comprobamos si el usuario ya existe
    if(os.path.isdir(path_user)):
        # flash("El usuario ya existe")
        error="El usuario ya existe"
            # si hay cookie
        cookie = request.cookies.get("usuario")
        if cookie == None:
            return render_template('acceso.html', title = "Acceso", cookie="", error=error)
        return render_template('acceso.html', title = "Acceso", user=cookie, error=error)
    
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

    # guardar cookies
    cookie=make_response(redirect(url_for('principal')))
    cookie.set_cookie("usuario",usuario)

    return cookie



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
    # return render_template('carrito.html', title = "Pelicula", movies=carrito, total="{0:.2f}".format(total))
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
        return render_template('principal.html', total=total, error="Saldo insuficiente",movies=catalogue['peliculas'],title = "Home")
    
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
    return render_template('principal.html', total=total, error="Compra procesada correctamente",movies=catalogue['peliculas'],title = "Home")



@app.route('/historialcompras', methods=['GET', 'POST'])
def historialcompras():

    if 'usuario' not in session:
        error="Por favor, primero inicie sesión"
            # si hay cookie
        cookie = request.cookies.get("usuario")
        if cookie == None:
            return render_template('acceso.html', title = "Acceso", cookie="", error=error)
        return render_template('acceso.html', title = "Acceso", user=cookie, error=error)
        
    
    nombre = session['usuario']
    usuario=session['usuario']
    app_folder = os.getcwd()
    path_user=os.path.join(app_folder, "si1users", usuario)

    catalogue_data = open(os.path.join(path_user,'compras.json'), encoding="utf-8").read()

    if not catalogue_data:
        catalogue = {'peliculas':[]}
    else:
        catalogue = json.loads(catalogue_data)

    path_datos=os.path.join(path_user, "datos.dat")

    dat = open(path_datos, 'r' ,encoding='utf-8')
    content = dat.readlines() 
    saldo=content[4]
    saldo=saldo[0:(len(saldo)-1)]
    dat.close()

    saldo="{0:.2f}".format(float(saldo))

    return render_template('historialcompras.html', title = "Historial", movies=catalogue['peliculas'], saldo=saldo)

@app.route('/aumento_saldo', methods=['POST'])
def aumento_saldo():

    aumento_saldo = request.form['aumento_saldo']

    usuario=session['usuario']
    app_folder = os.getcwd()
    path_user=os.path.join(app_folder, "si1users", usuario)
    path_datos=os.path.join(path_user, "datos.dat")

    dat = open(path_datos, 'r' ,encoding='utf-8')
    content = dat.readlines() 
    saldo=content[4]
    saldo=saldo[0:(len(saldo)-1)]
    content[4]=str(float(saldo)+float(aumento_saldo))
    datos_string= content[0]+content[1]+content[2]+content[3]+content[4]
    dat.close()

    open(path_datos, 'w' ,encoding='utf-8').write(datos_string)
    


    return redirect(url_for('historialcompras'))



@app.route('/usu_conectados', methods=['GET', 'POST'])
def usu_conectados():
    return str(random.randint(1, 50))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('usuario', None)
    session.pop('carrito', None)
    session.modified = True
    return redirect(url_for('principal'))
