# -*- coding: utf-8 -*-

import os
import sys, traceback
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



