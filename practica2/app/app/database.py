# -*- coding: utf-8 -*-

import os
import sys, traceback
import math
import random
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text
from sqlalchemy.sql import select

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False)
db_meta = MetaData(bind=db_engine)

# cargar tablas
db_table_movies = Table('imdb_movies', db_meta, autoload=True, autoload_with=db_engine)
db_table_orders = Table('orders', db_meta, autoload=True, autoload_with=db_engine)
db_table_products = Table('products', db_meta, autoload=True, autoload_with=db_engine)
db_table_orderdetail = Table('orderdetail', db_meta, autoload=True, autoload_with=db_engine)
db_table_customers = Table('customers', db_meta, autoload=True, autoload_with=db_engine)




############################## PAGINA PRINCIPAL ##############################


# getTopSales
def db_topSales():
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        # Seleccionar las topSales, limite 10
        db_result = db_conn.execute("SELECT * FROM getTopSales(2020,2021) LIMIT 10")
        db_conn.close()
        
        return list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'


# getMovieSelection
def db_movieSelection():
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        # Escoger una seleccion de productos
        db_result = db_conn.execute("SELECT prod_id, movietitle FROM public.imdb_movies INNER JOIN public.products on public.imdb_movies.movieid = public.products.movieid LIMIT 12")
        db_conn.close()

        # conseguir los datos
        result = []
        for fila in db_result:
            d = dict()
            d['prod_id'] = fila[0]
            d['title'] = str(fila[1])
            result.append(d)
        
        return result
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'


# busqueda y filtrado de peliculas
def db_searchFilterMovies(search, filter):

    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        # solo busqueda
        if search != "" and filter == "":
            db_result = db_conn.execute("SELECT public.products.prod_id, public.imdb_movies.movietitle " +
                    "FROM public.products INNER JOIN public.imdb_movies" + 
                    " ON public.products.movieid = public.imdb_movies.movieid "+
                    "WHERE lower(public.imdb_movies.movietitle) like '%%"+str(search)+"%%' LIMIT 20")

        # solo filtro
        elif search == "" and filter != "":
            db_result = db_conn.execute("SELECT public.products.prod_id, public.imdb_movies.movietitle "+
            "FROM public.products INNER JOIN public.imdb_movies ON public.products.movieid = public.imdb_movies.movieid "+
            "INNER JOIN public.imdb_moviegenres ON public.products.movieid = public.imdb_moviegenres.movieid "+
            "WHERE public.imdb_moviegenres.genreid = "+str(filter) + "LIMIT 20")

        # busqueda y filtro
        elif search != "" and filter != "":
            db_result = db_conn.execute("SELECT public.products.prod_id, public.imdb_movies.movietitle "+
            "FROM public.products INNER JOIN public.imdb_movies ON public.products.movieid = public.imdb_movies.movieid "+
            "INNER JOIN public.imdb_moviegenres ON public.products.movieid = public.imdb_moviegenres.movieid "+
            "WHERE public.imdb_moviegenres.genreid = "+str(filter) + 
            " and lower(public.imdb_movies.movietitle) like '%%"+str(search)+"%%' LIMIT 20")


        # ni busqueda ni filtro
        else:
            db_conn.close()
            return db_movieSelection()

        db_conn.close()

        result = []
        for fila in db_result:
            d = dict()
            d['prod_id'] = fila[0]
            d['title'] = str(fila[1])
            result.append(d)

        return result

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'



# getGenres
def db_getGenres():
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        # Escoger una seleccion de productos
        db_result = db_conn.execute("SELECT genreid, genre FROM public.imdb_genres")
        db_conn.close()

        # conseguir los datos
        result = []
        for fila in db_result:
            d = {}
            d['genreid'] = str(fila[0])
            d['genre'] = str(fila[1])
            result.append(d)
        
        return result
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'






############################## DETALLE DE LA PELICULA ##############################


# getMovieData 
def db_movieData(id):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        # CONSEGUIR LOS DATOS DEL PRODUCTO

        d = {}

        # imdb_movies: movietitle, year
        db_result = db_conn.execute("SELECT movietitle, year" +
                                    " FROM public.imdb_movies INNER JOIN public.products " +
                                    "ON public.imdb_movies.movieid =public.products.movieid "
                                    + "WHERE public.products.prod_id = " + str(id))

        for fila in db_result:
            d['movietitle'] = str(fila[0])
            d['year'] = str(fila[1])


        # products: price, description
        db_result = db_conn.execute("SELECT price, description FROM public.products" + 
                                    " WHERE prod_id = "+ str(id))

        for fila in db_result:
            d['price'] = str(fila[0])
            d['description'] = str(fila[1])


        # get directors
        db_result = db_conn.execute("SELECT public.imdb_directors.directorname FROM public.products " +
                "INNER JOIN public.imdb_directormovies ON public.products.movieid = public.imdb_directormovies.movieid "+
                "INNER JOIN public.imdb_directors ON public.imdb_directors.directorid = public.imdb_directormovies.directorid "
                + "WHERE public.products.prod_id = " + str(id))

        d['directors']=[]
        for fila in db_result:
            d['directors'].append(str(fila[0]))


        # get actors
        db_result = db_conn.execute("SELECT public.imdb_actors.actorname FROM public.products " +
                "INNER JOIN public.imdb_actormovies ON public.products.movieid = public.imdb_actormovies.movieid "+
                "INNER JOIN public.imdb_actors ON public.imdb_actors.actorid = public.imdb_actormovies.actorid "
                + "WHERE public.products.prod_id = " + str(id) + " LIMIT 7")

        d['actors']=[]
        for fila in db_result:
            d['actors'].append(str(fila[0]))


        # inventory: sales, stock
        db_result = db_conn.execute("SELECT sales, stock FROM public.inventory WHERE public.inventory.prod_id = " + str(id))

        for fila in db_result:
            d['sales'] = str(fila[0])
            d['stock'] = str(fila[1])


        # get language
        db_result = db_conn.execute("SELECT public.imdb_languages.language FROM public.imdb_languages "+
                "INNER JOIN public.imdb_movielanguages ON public.imdb_languages.languageid = public.imdb_movielanguages.languageid "
                + "INNER JOIN public.products ON public.imdb_movielanguages.movieid = public.products.movieid " + 
                "WHERE public.products.prod_id = " + str(id))

        d['languages']=[]
        for fila in db_result:
            d['languages'].append(str(fila[0]))


        # get genre
        db_result = db_conn.execute("SELECT public.imdb_genres.genre FROM public.imdb_genres "+
                "INNER JOIN public.imdb_moviegenres ON public.imdb_genres.genreid = public.imdb_moviegenres.genreid "
                + "INNER JOIN public.products ON public.imdb_moviegenres.movieid = public.products.movieid " + 
                "WHERE public.products.prod_id = " + str(id))

        d['genres']=[]
        for fila in db_result:
            d['genres'].append(str(fila[0]))


        # get country
        db_result = db_conn.execute("SELECT public.imdb_countries.country FROM public.imdb_countries "+
                "INNER JOIN public.imdb_moviecountries ON public.imdb_countries.countryid = public.imdb_moviecountries.countryid "
                + "INNER JOIN public.products ON public.imdb_moviecountries.movieid = public.products.movieid " + 
                "WHERE public.products.prod_id = " + str(id))

        d['countries']=[]
        for fila in db_result:
            d['countries'].append(str(fila[0]))

        db_conn.close()

        return d
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'



# valorar
def db_valorar(prodid, customerid, rating):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        # buscar el movie id
        db_result = db_conn.execute("SELECT public.imdb_movies.movieid " +
                    "FROM public.imdb_movies INNER JOIN public.products " +
                    "ON public.imdb_movies.movieid = public.products.movieid " +
                    "WHERE public.products.prod_id = " + str(prodid))

        for fila in db_result:
            movieid = str(fila[0])

        print("este es mi movie id " + movieid)

        # comprobar si hay entrada de movieid-customerid en ratings
        db_result = db_conn.execute("SELECT * FROM public.ratings "+
                    "WHERE movieid = "+ movieid +" and customerid = " + str(customerid))

        # no hay entrada: insert
        if len(list(db_result)) == 0:
            db_conn.execute("INSERT INTO public.ratings " +
                    "VALUES ("+movieid+","+str(customerid)+","+str(rating)+")")

        # hay entrada: update
        else:
            print("existo")
            db_conn.execute("UPDATE public.ratings SET rating = "+str(rating)+
                    " WHERE movieid = "+movieid+ "and customerid = "+ str(customerid))

        db_conn.close()
      
        return
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'



# getRatings
def db_getRatings(prodid):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        print("este es mi prodid " +str(prodid))
        
        # Escoger una seleccion de productos
        db_result = db_conn.execute("SELECT public.imdb_movies.ratingmean, public.imdb_movies.ratingcount "+
                    "FROM public.imdb_movies INNER JOIN public.products " +
                    "ON public.imdb_movies.movieid = public.products.movieid " 
                    + "WHERE public.products.prod_id =" + str(prodid))

        db_conn.close()

        # conseguir los datos
        for fila in db_result:
            d = {}
            d['ratingmean'] = str(fila[0])
            d['ratingcount'] = str(fila[1])
        
        return d
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'



############################## PAGINA ACCESO Y REGISTRO ##############################


def db_user_exists(usuario):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        # Comprobamos que el usuario existe
        db_user = db_conn.execute("SELECT * FROM public.customers WHERE username ='"+usuario+"'")
        db_user1 = db_conn.execute("SELECT * FROM public.customers WHERE username='elena'")

        db_conn.close()

        if db_user.rowcount == 0:
            return False

        return True
        
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'



def db_user_login(usuario, password):
    try:
        #conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        db_pass = db_conn.execute("SELECT password FROM customers WHERE username ='"+usuario+"'")
        rows = db_pass.fetchall()
        

        #Puede haber varios usuarios con el mismo nombre
        for row in rows:
            pass1=row[0]
            print(pass1)
            print(password)
            if pass1==password:
                db_customerid = db_conn.execute("SELECT customerid FROM public.customers WHERE username ='"+usuario+"' AND password='"+password+"'")
                res = db_customerid.fetchall()
                customerid = res[0][0]
                return True, customerid
      
        db_conn.close()
        return False, 0

        
        
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'



def db_user_register(adress, email, creditcard, username, password):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        if(db_user_exists(username)==True):
            return False
 
        db_last_customer_id = db_conn.execute("SELECT MAX(customerid) FROM public.customers")
        rows = db_last_customer_id.fetchall()
        last_customer_id=rows[0][0]
        customerid = last_customer_id + 1
        balance=random.randint(0, 100)
        print(balance)
      
        db_conn.execute("INSERT INTO public.customers VALUES ('"+str(customerid)+"', '"+adress+"', '"+email+"', '"+creditcard+"','"+username+"','"+str(balance)+"', '"+password+"')")
        db_conn.close()

        return True, customerid
        
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'



############################## PAGINA HISTORIAL COMPRA ##############################


def db_get_saldo(customerid):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        
        db_balance = db_conn.execute("SELECT balance FROM public.customers WHERE customerid ='"+customerid+"'")
        rows = db_balance.fetchall()
        balance=rows[0][0]

        db_conn.close()

        return balance
        
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'


def db_increase_saldo(customerid, aumento_saldo):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        nuevo_saldo = db_get_saldo(usuario) + int(aumento_saldo)        
        db_conn.execute("UPDATE public.customers SET balance = '"+str(nuevo_saldo)+ "' WHERE customerid= '"+customerid+"'")
        db_conn.close()

        return True
        
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'



def db_historial(customer_id):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        #Queremos agrupar las odenes por orderid ya que es la clave primaria
        #Primero habia pensado en hacerlo por fecha pero es que hay fechas de compra del mismo dia pero con distinto order id
        db_orderid = db_conn.execute("SELECT orderid FROM orders WHERE customerid='"+str(customer_id)+"'")
        rows = db_orderid.fetchall()
        print("LO QUE QUEREMOS METER EN LA TABLA ------------------------------")
        print(rows)
        
        #creamos una lista para almacenar los datos
        compras_cliente=[]

        for orderid in rows:

            print(orderid[0])

            db_compras = db_conn.execute("SELECT B.orderdate, E.movietitle, E.year, D.price \
                                            FROM public.customers AS A \
                                                INNER JOIN public.orders AS B on A.customerid = B.customerid \
                                                INNER JOIN public.orderdetail AS C on C.orderid = B.orderid \
                                                INNER JOIN public.products as D on C.prod_id = D.prod_id \
                                                INNER JOIN public.imdb_movies as E on E.movieid = D.movieid \
                                            WHERE A.customerid = '"+str(customer_id)+"' and B.orderid='"+str(orderid[0])+"' \
                                            ORDER BY B.orderid")

            
            rows = db_compras.fetchall()

            compras_orderid= {"orderid": orderid[0], "orderdate":str(rows[0][0]), "pelis_compra":[] }
            
            for row in rows:
                pelis={"movietitle": row[1], "year": row[2], "price":int(row[3])}
                compras_orderid["pelis_compra"].append(pelis)

            compras_cliente.append(compras_orderid)
        
   
        compras_cliente=sorted(compras_cliente, key=lambda key : key["orderdate"], reverse=True)
        print(compras_cliente)
        db_conn.close()

        return compras_cliente
        
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'




############################## PAGINA CARRITO ##############################

def db_show_carrito(customerid):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
 
        db_orderid = db_conn.execute("SELECT orderid FROM orders WHERE customerid='"+customerid+"' AND status is NULL")
        rows = db_orderid()
        orderid=rows[0][0]    
        

        db_orderid = db_conn.execute("SELECT C.prod_id, D.movietitle, B.quantity \
                                        FROM public.orders as A \
                                            INNER JOIN public.orderdetail AS B on A.orderid = B.orderid \
                                            INNER JOIN public.products as C on B.prod_id = C.prod_id \
                                            INNER JOIN public.imdb_movies as D on C.movieid = D.movieid \
                                        WHERE A.orderid=1 \
                                        ORDER BY A.orderid")

        db_conn.close()

        return True
        
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'









