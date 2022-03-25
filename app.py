
from time import sleep
from turtle import heading
from flask import Flask, redirect,render_template, request,flash,session
from flask_sqlalchemy import SQLAlchemy
import os

app=Flask(__name__)
db=SQLAlchemy(app)

# app.config['SQLALCHEMY_DATABASE_URI']='mssql+pyodbc://DESKTOP-3P0102M\SQLEXPRESS/TaqiComputers_DB?driver=SQL+Server?trusted_connection=yes'
app.secret_key=os.urandom(20)

from dbconnection import DbConnection
conn=DbConnection()
conn.connectToDb() 
cursor=conn.getCursor()



headings=(("id"),("Name"),("Image"))
# data=[]
# for row in personData:
#     data.append(row)

# main area
# home page route
@app.route('/home')
def homePage():

    if 'userid' in session:
        cursor.execute("Select * from tbPerson")    
        personData=cursor.fetchall()
        print(personData)
        
        imagesPath=[]
        basePath='static/images'
        train_dir = os.listdir(basePath)
        for person in train_dir:
            pix = os.listdir("static/images/" + person)
            # for person_img in pix:
            
            imagesPath.append('images'+'/'+str(person)+'/'+pix[0])
            print(imagesPath)
        for i in range(len(personData)):
            personData[i][-1]=imagesPath[i]
            # print(os.path.join(str(pix),pix[0]))
        
        return render_template('home.html',headings=headings,data=personData)
    
    else:
        return redirect('/')



# route for login page
@app.route('/')
def login():
    return render_template('login.html')

# route for login post
@app.route('/login_validation',methods=['POST'])
def login_validation():
    email= request.form.get('email')
    password=request.form.get('password1')

    cursor.execute("select * from tbAdmins where email = ? and password = ?",email,password)
    adminData=cursor.fetchall()

    # check if we found match
    if len(adminData)>0:
        session['userid']=adminData[0][0]
        return redirect('/home')

    else:
        return render_template('login.html')
    
    
# route for signup page
@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup',methods=['POST'])
def signUser():
    email= request.form.get('email')
    password1=request.form.get('password1')
    password2=request.form.get('password2')
    message="Successfully Registered!"
    if password1==password2 :
        cursor.execute("insert into tbAdmins values(?,?)",email,password1)
        
        flash(message)
        sleep(2)
        return redirect('/')

    else:
        message="Passwords Donot Match"
        flash()
        return redirect('/signup')


@app.route('/logout')
def logout():
    session.pop('userid')
    sleep(2)
    flash('Logged out Sucessfully')
    
    return redirect('/')


if __name__=="__main__":
    app.run(debug=True)