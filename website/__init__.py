import imp
from flask import Flask, redirect,render_template, request,flash,session,Response

import os
# from main import startProject
from .dbconnection import DbConnection
from .training import trainingImages


def createApp():
    # trainingImages()
    app=Flask(__name__)

    app.secret_key=os.urandom(20)

    from .views import views
    app.register_blueprint(views,url_prefix='/')
    return app



def connectToDb():
    conn=DbConnection()
    conn.connectToDb() 
    cursor=conn.getCursor()
    return cursor