from time import sleep, time
from cv2 import VideoCapture
from flask import Blueprint, redirect, render_template, request, flash, session, Response
import pandas as pd, numpy as np
from . import connectToDb
from .crdoperations import UsersGetting
import folium, cv2, os
from .CameraFile import cameraThread, mainWorking
from sklearn.model_selection import train_test_split
from sklearn import linear_model
cursor = connectToDb()
views = Blueprint('views', __name__)
camerasList = [
 0, 1]

def find_camera(list_id):
    return camerasList[int(list_id)]


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


@views.route('/user/<user_id>')
def userDetail(user_id):
    print(user_id)
    users = UsersGetting(cursor)
    allRecords = users.getAllLocationRecord(user_id)
    print(allRecords)
    location = predictNewLocation(cursor, user_id)
    map = folium.Map(location=[24.79387658, 67.1351927], min_zoom=18, zoom_start=14, height=350, width=600, min_lat=24.6, max_lat=24.8, min_lon=66, max_lon=67.15, left='20%', top='10%', zoom_control=True)
    for row in allRecords:
        print(row)
        tooltip = str(row[1])
        folium.Circle(location=[
         row[(-2)], row[(-1)]],
          radius=2,
          popup=(str(row[0])),
          color='#3186cc',
          fill=True,
          fill_color='#3186cc').add_to(map)
        map.save('website/templates/map.html')

    return render_template('userdetail.html', uid=user_id, userLocationRecord=allRecords, location=location)


@views.route('/')
def login():
    return render_template('login.html')


@views.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password1')
    cursor.execute('select * from tbAdmins where email = ? and password = ?', email, password)
    adminData = cursor.fetchall()
    if len(adminData) > 0:
        session['userid'] = adminData[0][0]
        return redirect('/home')
    return render_template('login.html')


@views.route('/signup')
def signup():
    return render_template('signup.html')


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
    flash()
    return redirect('/signup')


@views.route('/logout')
def logout():
    session.pop('userid')
    sleep(2)
    flash('Logged out Sucessfully')
    return redirect('/')


@views.route('/cameras')
def cameras():
    return render_template('cameras.html', cameraList=camerasList)


@views.route('/video/<string:id>', methods=['GET', 'POST'])
def video(id):
    return Response((genFrames(id)), mimetype='multipart/x-mixed-replace; boundary=frame')


def genFrames(camid):
    cursor1 = connectToDb()
    users = UsersGetting(cursor1)
    userids = users.gettingUserId()
    cam = find_camera(camid)
    video_capture = cv2.VideoCapture(cam, cv2.CAP_DSHOW)
    try:
        while True:
            frame = mainWorking(video_capture, cam, userids, cursor1)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'

    except Exception as e:
        
        print(e)
        


def predictNewLocation(cursor, userId):
    userLocations = UsersGetting(cursor).getUserLocationNameOrdered(userId)
    print(len(userLocations))
    df = pd.DataFrame(userLocations)

    df = pd.DataFrame((np.reshape(userLocations, (df.shape[0], 3))), columns=['locid', 'locName', 'time'])
    df['time'] = df['time'].astype(float)
    print(df['time'])
    X_train, X_test, y_train, y_test = train_test_split((df[['time']]), (df.locName), train_size=0.8)
    model = linear_model.LogisticRegression()
    model.fit(X=X_train, y=y_train)
    newLoc = model.predict(X_test)

    return newLoc