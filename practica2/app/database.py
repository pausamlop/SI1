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
        
        # Escoger una seleccion de peliculas
        db_result = db_conn.execute("SELECT * FROM public.imdb_movies LIMIT 12")
        db_conn.close()

        print(db_result)
 
        
        return list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'
