#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from app import database
from flask import render_template, request, url_for
import os
import sys
import time

@app.route('/', methods=['POST','GET'])
@app.route('/index', methods=['POST','GET'])
def index():
    return render_template('index.html')


@app.route('/borraEstado', methods=['POST','GET'])
def borraEstado():
    if 'state' in request.form:
        state    = request.form["state"]
        bSQL    = request.form["txnSQL"]
        bCommit = "bCommit" in request.form
        bFallo  = "bFallo"  in request.form
        duerme  = request.form["duerme"]
        dbr = database.delState(state, bFallo, bSQL=='1', int(duerme), bCommit)
        return render_template('borraEstado.html', dbr=dbr)
    else:
        return render_template('borraEstado.html')

    
@app.route('/topUK', methods=['POST','GET'])
def topUK():

    topUK = database.getMongoCollection(database.mongo_client)

    list1=[]
    list2=[]
    list3=[]

    query1 = {"$and":[{"year":{"$gte":"1990","$lte":"1992"}},{"genres":"Comedy"}]}
    result1 = topUK.find(query1)
    for x in result1:
        list1.append(x)


    query2 = {"$and":[{"year":{"$in":["1995","1997","1998"]}},{"genres":"Action"},{"title":{"$regex":", The"}}]}
    result2 = topUK.find(query2)
    for y in result2:
        list2.append(y)

    query3 = {"$and":[{"actors":{"$regex":"McAree, Darren"}},{"actors":{"$regex":"Lockett, Katie"}}]}
    result3 = topUK.find(query3)
    for z in result3:
        list3.append(z)
    
    movies=[list1,list2, list3]
    

    return render_template('topUK.html', movies=movies)