
from datetime import datetime
import pickle
from re import M
from time import sleep, time
from tkinter import Canvas
from turtle import color
from xmlrpc.client import DateTime
from cv2 import VideoCapture, dft
from flask import Blueprint, jsonify, make_response, redirect, render_template, request, flash, send_file, session, Response
import pandas as pd
import numpy as np

from website.dbConnection import DbConnection
from . import connectToDb
from .crudOperations import UserInsertion, UsersGetting
import folium
import cv2
import os
import io
from .cameraFile import CameraWork

from sklearn import linear_model
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from datetime import date
import gmplot
from threading import Thread
from sklearn.model_selection import train_test_split
from sklearn import metrics


apikey = 'AIzaSyDXKvA6U5_v_iCMdyZH_XODboqJ8ivyfSM'

matplotlib.use('Agg')

# db cursor
cursor = connectToDb()

# making a blueprint
views = Blueprint('views', __name__)

# route for Home page
# ----------------------------------------------

@views.route('/home')
def homePage():

    headings = ('id', 'Name', 'Image')
    if 'userid' in session:
        cursor.execute('Select * from tbPerson')
        personData = cursor.fetchall()
        # print(personData)
        imagesPath = []
        basePath = 'website/static/images'
        train_dir = os.listdir(basePath)
        for person in train_dir:
            pix = os.listdir('website/static/images/' + person)
            imagesPath.append('images/' + str(person) + '/' + pix[0])
            print(imagesPath)

        for i in range(len(personData)):
            personData[i][-1] = imagesPath[i]

        return render_template('home.html', headings=headings, data=personData)
    return redirect('/')


# route for userdetail page
# ----------------------------------------------
@views.route('/users/<user_id>', methods=['GET', 'POST'])
def userDetail2(user_id):
    users = UsersGetting(cursor)
    # get user image

    userRecord = users.getSpecificUser(user_id)
    pix = os.listdir('website/static/images/' + userRecord)
    imagePath = 'images/'+userRecord+'/'+pix[0]

    # userData=loadUserdata(user_id)

    # modelTraining(user_id)
    # check if request=post
    try:
        if request.method == 'POST':

            sDate = request.form['cdate']
            sDate = datetime.strptime(sDate, '%Y-%m-%d').strftime('%d/%m/%y')
            print(type(sDate))
            sDateLocations = users.getSpecificDateLocations(user_id, sDate)
            sDate = datetime.strptime(sDate, '%d/%m/%y').strftime('%d-%m-%y')
            print(sDateLocations)
            print(sDate)

            map = plotmap(sDateLocations)
            map2 = plotmap2(sDateLocations)
            map.save('website/templates/map.html')
            map2.draw('website/templates/map2.html')
            return render_template('userdetail.html', uid=user_id, userLocationRecord=sDateLocations, sdate=sDate, imageurl=imagePath)
        # return redirect('/users/<user_id>')

        # nextLoc=predictNextLocation(int(user_id),sDate)
        # sDateTimeChart=barchart(user_id,sDate)

        else:
            currentDateRecords = users.getCurrentDateLocations(int(user_id))

            # nextLoc=predictNextLocation(int(user_id),sDate)
            map = plotmap(currentDateRecords)
            map.save('website/templates/map.html')
            map2 = plotmap2(currentDateRecords)
            map2.draw('website/templates/map2.html')

            return render_template('userdetail.html', uid=user_id, userLocationRecord=currentDateRecords, imageurl=imagePath)
    except:
        print('CSomething wrong')
    return render_template('userdetail.html', imageurl=imagePath)


# route for showing map
# ----------------------------------------------
@views.route('/showmap')
def showmap():
    return render_template('map2.html')


def plotmap(records):
    map = folium.Map(location=[24.79387658, 67.1351927], max_zoom=18, zoom_start=14, height=300, width='60%',
                     min_lat=24.6, max_lat=24.8, min_lon=66, max_lon=67.15, left='20%', top='5%', zoom_control=True)

    for row in records:
        # print(row)
        # tooltip = str(row[1])
        folium.Circle(location=[
            row[-3], row[-2]],
            radius=2,
            popup=folium.Popup(
                f"<h4>Location: {row[0]}</h4><p>Latitude: {row[-3]}</p> <p>Latitude: {row[-2]}</p>"),
            color='#3186cc',
            fill=True,
            fill_color='#3186cc').add_to(map)

    folium.TileLayer('stamenwatercolor').add_to(map)
    folium.TileLayer('stamenterrain').add_to(map)
    folium.TileLayer('openstreetmap').add_to(map)
    folium.LayerControl().add_to(map)

    return map


def plotmap2(records):
    gmap = gmplot.GoogleMapPlotter(24.79387658, 67.1351927, 16)
    gmap.apikey = apikey
    latlist = []
    longList = []
    for row in records:
        latlist.append(float(row[-3]))
        longList.append(float(row[-2]))

    gmap.scatter(latlist, longList, '#FF0000', size=20)
    gmap.plot(latlist, longList, 'cornflowerblue', edge_width=3.0)

    return gmap


# route for login get
# ----------------------------------------------
@views.route('/')
def login():
    return render_template('login.html')

# route for login Post
# ----------------------------------------------


@views.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password1')
    cursor.execute(
        'select * from tbAdmins where email = ? and password = ?', email, password)
    adminData = cursor.fetchall()

    if len(adminData) > 0:
        # add user id to session
        session['userid'] = adminData[0][0]

        return redirect('/home')

    return render_template('login.html')


# route for signup get
# ----------------------------------------------
@views.route('/signup')
def signup():
    return render_template('signup.html')

# route for signup Post
# ----------------------------------------------


@views.route('/signup', methods=['POST'])
def signUser():
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    message = 'Successfully Registered!'
    if password1 == password2:
        cursor.execute('insert into tbAdmins values(?,?)', email, password1)
        flash(message)
        return redirect('/')
    message = 'Passwords Donot Match'
    flash(message)
    return redirect('/signup')


# route for logging out
# ----------------------------------------------
@views.route('/logout')
def logout():
    session.pop('userid')

    flash('Logged out Sucessfully')
    return redirect('/')


# route for camera feed page
# ----------------------------------------------
@views.route('/cameras')
def cameras():
    return render_template('cameras.html')


# routes for getting camera feed
# ----------------------------------------------
@views.route('/video1', methods=['GET'])
def video1():
    return Response((genFrames()), mimetype='multipart/x-mixed-replace; boundary=frame')


@views.route('/video2', methods=['GET'])
def video2():
    return Response((genFrames2()), mimetype='multipart/x-mixed-replace; boundary=frame')


# getting frames from camera recognizing faces
def genFrames():
    video_capture1 = cv2.VideoCapture(0)
    cursor1 = connectToDb()
    users = UsersGetting(cursor1)
    userids = users.gettingUserId()
    camera1 = CameraWork(video_capture1, 2, userids, cursor1)
    try:
        while True:

            sucess, frame = video_capture1.read()
            frame = camera1.mainWorking()

            ret, buffer = cv2.imencode('.jpg', frame)

            frame = buffer.tobytes()
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'

    except Exception as e:

        print(e)
# receive frames from


def genFrames2():
    video_capture2 = cv2.VideoCapture(1)
    cursor2 = connectToDb()
    users = UsersGetting(cursor2)
    userids = users.gettingUserId()
    camera2 = CameraWork(video_capture2, 3, userids, cursor2)
    try:
        while True:
            sleep(0.01)
            sucess, frame2 = video_capture2.read()
            frame2 = camera2.mainWorking2()

            ret2, buffer2 = cv2.imencode('.jpg', frame2)

            frame2 = buffer2.tobytes()
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame2 + b'\r\n'

    except Exception as e:

        print(e)


# route for barchart showing timespend by user
# ----------------------------------------------
@views.route('/barchart2/<userid>/<sdate>', methods=['GET', 'POST'])
def barchart2(userid, sdate):
    try:
        sdate = datetime.strptime(sdate, '%d-%m-%y').strftime('%d/%m/%y')
        print("Today:", sdate)

        users = UsersGetting(cursor)
        timespends = users.getSpecificDateTimespend(userid, sdate)
        print(timespends)
        timespend = np.zeros(5)
        for row in timespends:
            print(row.locId)
            timespend[row.locId-1] = row.timeSpend
        if len(timespend) < 3:
            timespend.append(0)
        print("TimeSpends:", timespend)

        print('H:', userid)
        Location = ['Main Entrance', 'Cafeteria',
                    'SportsArea', 'Tuc Shop', 'Library']

        ypos = np.arange(len(Location))
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.set_title("User Daily Record")
        # ax.legend()
        ax.set_xticks(ypos, Location)
        ax.set_xlabel('Locations')
        ax.set_ylabel('Time Spend(min)')
        ax.bar(ypos, timespend)
        canvas = FigureCanvas(fig)
        img = io.BytesIO()
        fig.savefig(img)
        img.seek(0)
        return send_file(img, mimetype='img/png')
    except:
        print('Cannot convert dateformat twice')


# route for Locations page
# ----------------------------------------------
@views.route('/locations')
def locations():
    queryobject = UsersGetting(cursor)
    allLocations=queryobject.getAllLocations()

    return render_template('locations.html',locations=allLocations)


# route for prediction page
# ----------------------------------------------
@views.route('/predictionpage')
def predictionpage():

    queryobject = UsersGetting(cursor)
    users = queryobject.gettingUserId()

    return render_template('predictions.html', users=users)


@views.route('/predictUserPath/<userid>/<date>', methods=['GET', 'POST'])
def predictUserPath(userid, date):
    print(userid, date)
    weekday = datetime.strptime(date, '%Y-%m-%d').date().weekday()+1
    print(weekday)
    model = None

    queryobject = UsersGetting(cursor)
    locationNames = queryobject.getLocationNames()
    
    if weekday < 5 and weekday > 0:
        print(locationNames)
        with open(f'./website/static/models/user_{userid}_model', 'rb') as f:
            model = pickle.load(f)

            pred = model.predict([[weekday]])
            userpath=[]
            for i in range(1,len(pred[0]),3):
                print('i: ',pred[0][i])
                userpath.append(locationNames[int(pred[0][i])-1])
            print(type(pred[0]))

    return jsonify(userpath)


# route for getting data and modify for training
# ----------------------------------------------
@views.route('/loaduserdata/<userid>')
def loaduserdata(userid):
    data = []
    queryobject = UsersGetting(cursor)
    users = queryobject.getUserAllLocations(userid)
    for row in users:
        data.append([x for x in row])
    print(type(data[0]))

    # making a df
    df1 = pd.DataFrame(
        data, columns=['locId', 'personId', 'date', 'time', 'lat', 'long', 'timespend'])
    print(df1)
    df1['date'] = pd.to_datetime(df1['date'], format='%d/%m/%y')
    df1['dayOfWeek'] = df1['date'].dt.dayofweek+1
    userdates = df1['date'].drop_duplicates()

    # make arrays for path and days
    paths = []
    days = []
    df1['date'].drop_duplicates()
    # for udate in df2['date'].unique():
    for udate in userdates:

        # append locations to path where date == udate
        path1 = df1['locId'][df1['date'] == udate].values
        path1 = path1.tolist()
        paths.append(path1)
        print(type(udate.dayofweek))
        days.append(udate.dayofweek+1)

    data2 = {
        'userpath': paths,
        'dayofweek': days
    }

    dfPred = pd.DataFrame(data2)
    dfPred.info()
    print(dfPred)

    # write csvfile
    dfPred.to_csv(
        f'./website/static/csvs/user_{userid}_data.csv', index=False, mode='w')

    return jsonify('Load Data success')


# route for trainin model with respect to userid
# ----------------------------------------------
@views.route('/trainingdata/<userid>')
def trainingdata(userid):
    df2 = pd.read_csv(f'./website/static/csvs/user_{userid}_data.csv')

    X = df2.iloc[:, [1]].values
    y = df2.iloc[:, 0].values
    y2 = df2.iloc[:, 0]

    # split dataset

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=8)
    # apply logistic regression
    from sklearn.linear_model import LogisticRegression

    clf = LogisticRegression(max_iter=1000)
    model = clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    print('Accuracy: ', metrics.accuracy_score(y_test, y_pred))

    # Saving model
    with open(f'./website/static/models/user_{userid}_model', 'wb') as f:
        pickle.dump(model, f)

    return jsonify('training completed')

# <locname>/<lat>/<long>/<file>

@views.route('/addLocation',methods=['GET','POST'])
def addLocation():
        
    dataGet=request.get_json(force=True)
    
    print(dataGet)
    locName=dataGet['locname']
    lat=dataGet['latitude']
    long=dataGet['longitude']

    queryobject = UserInsertion(cursor)
    queryobject.insertLocation(locName,lat,long)
    

    return jsonify('Location Saved Success') 


