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









# INSERT INTO public.customers (customerid, address, email, creditcard, username, password,balance) VALUES (DEFULT, 'rffffds', 'sdfsdfsdf', '11112222333344444','elenaaaaa','pass' , 0 );


# INSERT INTO public.customers VALUES (14094, 'rffffds', 'sdfsdfsdf', '11112222333344444','elenaaaaa','pass' , 0 );

# SELECT MAX(CUSTOMERID) FROM public.customers;

# DELETE FROM public.customers 
#     WHERE customerid = 222222222;

#     SELECT MAX(CUSTOMERID) FROM PUBLIC.CUSTOMERS;
#     SELECT COUNT(CUSTOMERID) FROM PUBLIC.CUSTOMERS;

# SELECT * FROM public.customers WHERE customerid=14904;

# UPDATE public.customers SET balance = floor(100 * random()) WHERE customerid=14094;

# SELECT * FROM public.customers WHERE username=elena;
# db_compras = db_conn.execute("SELECT B.orderdate, E.movietitle, E.year, D.price FROM public.customers AS A INNER JOIN public.orders AS B on A.customerid = B.customerid INNER JOIN public.orderdetail AS C on C.orderid = B.orderid INNER JOIN public.products as D on C.prod_id = D.prod_id INNER JOIN public.imdb_movies as E on E.movieid = D.movieid WHERE A.customerid = '"+str(customer_id)+"' and B.orderid='"+str(orderid[0])+"' ORDER BY B.orderid'")