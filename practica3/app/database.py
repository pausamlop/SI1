# -*- coding: utf-8 -*-

import os
import sys, traceback, time

from sqlalchemy import create_engine
from pymongo import MongoClient

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text
from sqlalchemy.sql import select, delete

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False, execution_options={"autocommit":False})
db_meta = MetaData(bind=db_engine)

# cargar tablas
db_table_orders = Table('orders', db_meta, autoload=True, autoload_with=db_engine)
db_table_orderdetail = Table('orderdetail', db_meta, autoload=True, autoload_with=db_engine)
db_table_customers = Table('customers', db_meta, autoload=True, autoload_with=db_engine)


# Crea la conexión con MongoDB
mongo_client = MongoClient()

def getMongoCollection(mongoDB_client):
    mongo_db = mongoDB_client.si1
    return mongo_db.topUK

def mongoDBCloseConnect(mongoDB_client):
    mongoDB_client.close()

def dbConnect():
    return db_engine.connect()

def dbCloseConnect(db_conn):
    db_conn.close()
  


def delState(state, bFallo, bSQL, duerme, bCommit):

    # TODO: Ejecutar consultas de borrado
    # - ordenar consultas según se desee provocar un error (bFallo True) o no
    # - ejecutar commit intermedio si bCommit es True
    # - usar sentencias SQL ('BEGIN', 'COMMIT', ...) si bSQL es True
    # - suspender la ejecución 'duerme' segundos en el punto adecuado para forzar deadlock
    # - ir guardando trazas mediante dbr.append()
    
    try:

        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        # Array de trazas a mostrar en la página
        dbr=[]

        # INICIO TRANSACCION
        dbr.append("Inicio de la transaccion.")

        if bSQL:
            db_conn.execute("BEGIN TRANSACTION")
        else:
            transaction = db_conn.begin()


        # ENCONTRAR CLIENTES A BORRAR
        dbr.append("Buscando clientes con estado " + str(state))

        if bSQL:
            db_result = db_conn.execute("SELECT customerid FROM public.customers WHERE state = '" + str(state)+"'")
        else:
            sqlAlchemy = select(db_table_customers.c.customerid).where(text("state = '" + str(state)+"'"))
            db_result = db_conn.execute(sqlAlchemy)

        # conseguir los datos
        customers = []
        for fila in db_result:
            customers.append(str(fila[0]))

        print("size of customers: " + str(len(customers)))

        # ENCONTRAR LAS ORDERS DE CADA CLIENTE
        dbr.append("Buscando las orders de los clientes.")
        orders = []
        for i in customers:
            if bSQL:
                db_result = db_conn.execute("SELECT orderid FROM public.orders WHERE customerid = " + i)
            else:
                sqlAlchemy = select(db_table_orders.c.orderid).where(text("customerid = " + i))
                db_result = db_conn.execute(sqlAlchemy)
            
            # conseguir los datos
            for fila in db_result:
                orders.append(str(fila[0]))

        # BORRAR LAS ORDERDETAIL DE CADA ORDER
        dbr.append("Borrando las orderdetail de las orders.")
        if bSQL:
            for i in orders:
                db_result = db_conn.execute("DELETE FROM public.orderdetail WHERE orderid = " + i)
        else:
            for i in orders:
                sqlAlchemy = delete(db_table_orderdetail).where(text("orderid = " + i))
                db_result = db_conn.execute(sqlAlchemy)

        # fallo de foreign key
        if bFallo:

            # COMMIT INTERMEDIO - se han eliminado solo las orderdetail
            if bCommit: 
                dbr.append("Efectuando commit intermedio.")
                
                if bSQL:
                    db_conn.execute("COMMIT")
                    db_conn.execute("BEGIN TRANSACTION")
                else:
                    transaction.commit()
                    transaction = db_conn.begin()

            # BORRAR LOS CLIENTES
            dbr.append("Borrando los clientes.")
            if bSQL:
                db_conn.execute(" DELETE FROM public.customers WHERE state = '" + str(state)+"'")
            else:
                sqlAlchemy = delete(db_table_customers).where(text("state = '" + str(state)+"'"))
                db_result = db_conn.execute(sqlAlchemy)

            # BORRAR LAS ORDERS DE CADA CLIENTE
            dbr.append("Borrando las orders de los clientes.")
            if bSQL:
                for i in orders:
                    db_result = db_conn.execute("DELETE FROM public.orders WHERE orderid = " + i)  
            else:
                for i in orders:
                    sqlAlchemy = delete(db_table_orders).where(text("orderid = " + i))
                    db_result = db_conn.execute(sqlAlchemy)
  
            
        # funcionamiento correcto
        else:

            time.sleep(duerme)

            # BORRAR LAS ORDERS DE CADA CLIENTE
            dbr.append("Borrando las orders de los clientes.")
            if bSQL:
                for i in orders:
                    db_result = db_conn.execute("DELETE FROM public.orders WHERE orderid = " + i)  
            else:
                for i in orders:
                    sqlAlchemy = delete(db_table_orders).where(text("orderid = " + i))
                    db_result = db_conn.execute(sqlAlchemy)
                
            # BORRAR LOS CLIENTES
            dbr.append("Borrando los clientes.")
            if bSQL:
                db_conn.execute(" DELETE FROM public.customers WHERE state = '" + str(state)+"'")
            else:
                sqlAlchemy = delete(db_table_customers).where(text("state = '" + str(state)+"'"))
                db_result = db_conn.execute(sqlAlchemy)


    except Exception as e:
        traceback.print_exc(file=sys.stderr)

        if db_conn is None:
            return ['Something is broken']
        
        dbr.append("Error - efectuando rollback.")

        if bSQL:
            db_conn.execute("ROLLBACK")
        else:
            transaction.rollback()
        
        db_conn.close()

    else:
        dbr.append("Transaccion correcta - efectuando commit.")

        if bSQL:
            db_conn.execute("COMMIT")
        else:
            transaction.commit()
        db_conn.close()

    return dbr

