
from flask import Flask, redirect,render_template, request,flash,session,Response
from flask_sqlalchemy import SQLAlchemy
import os
from .crdoperations import UsersGetting
import folium,cv2
# from main import startProject
from .dbconnection import DbConnection
from .training import trainingImages


conn=DbConnection()
conn.connectToDb() 
cursor=conn.getCursor()


app=Flask(__name__)

app.secret_key=os.urandom(20)



if __name__=="__main__":
    trainingImages()
    app.run(debug=True)
    