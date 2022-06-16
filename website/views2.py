
from datetime import datetime
from time import sleep, time
from tkinter import Canvas
from turtle import color
from cv2 import VideoCapture
from flask import Blueprint, redirect, render_template, request, flash, send_file, session, Response
import pandas as pd, numpy as np
from . import connectToDb
from .crdoperations import UsersGetting
import folium, cv2, os,io
from .CameraFile import cameraThread, mainWorking
from sklearn.model_selection import train_test_split
from sklearn import linear_model
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from datetime import date
import gmplot

apikey = 'AIzaSyDXKvA6U5_v_iCMdyZH_XODboqJ8ivyfSM'

matplotlib.use('Agg')

cursor = connectToDb()
views = Blueprint('views', __name__)
camerasList = [
 0, 1]

def find_camera(list_id):
    return camerasList[int(list_id)]


# homepage route

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



# user detail page route
@views.route('/users/<user_id>',methods=['GET','POST'])
def userDetail2(user_id):
    users = UsersGetting(cursor)
    # allRecords = users.getAllLocationRecord(user_id)
    # print(allRecords)
    # location = predictNewLocation(user_id)
    # check if request=post
    if request.method=='POST':
        sDate=request.form['cdate']
        sDateLocations=users.getSpecificDateLocations(user_id,sDate)
        print(sDate)
        # sDateTimeChart=barchart(user_id,sDate)
        map = plotmap2(sDateLocations)
        # map.save('website/templates/map.html')
        map.draw('website/templates/map2.html')
        return render_template('userdetail.html',uid=user_id,userLocationRecord=sDateLocations,sdate=sDate)
        # return redirect('/users/<user_id>')

    else:
        currentDateRecords=users.getCurrentDateLocations(int(user_id))

        map=plotmap2(currentDateRecords)
        # map.save('website/templates/map.html')
      
        map.draw('website/templates/map2.html')

        return render_template('userdetail.html', uid=user_id, userLocationRecord=currentDateRecords)


@views.route('/showmap')
def showmap():
    return render_template('map2.html')  


def plotmap(records):
    map=folium.Map(location=[24.79387658, 67.1351927], max_zoom=18, zoom_start=14, height=300, width='60%', min_lat=24.6, max_lat=24.8, min_lon=66, max_lon=67.15, left='20%', top='5%', zoom_control=True)
    for row in records:
        # print(row)
        # tooltip = str(row[1])
        folium.Circle(location=[
         row[-3], row[-2]],
          radius=2,
          popup=folium.Popup(f"<h4>Location: {row[0]}</h4><p>Latitude: {row[-3]}</p> <p>Latitude: {row[-2]}</p>"),
          color='#3186cc',
          fill=True,
          fill_color='#3186cc').add_to(map) 


        

    return map



def plotmap2(records):
    gmap=gmplot.GoogleMapPlotter(24.79387658, 67.1351927, 16)
    gmap.apikey=apikey
    latlist=[]
    longList=[]
    for row in records:
        latlist.append(float(row[-3]))
        longList.append(float(row[-2]))

    gmap.scatter(latlist,longList,'#FF0000',size = 20)
    gmap.plot(latlist, longList, 'cornflowerblue', edge_width = 3.0)
    
    return gmap

    
    

        



# login route
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


# signup route
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


# logging out
@views.route('/logout')
def logout():
    session.pop('userid')
    sleep(2)
    flash('Logged out Sucessfully')
    return redirect('/')



# camera feed route
@views.route('/cameras')
def cameras():
    return render_template('cameras.html', cameraList=camerasList)

# getting video
@views.route('/video1', methods=['GET', 'POST'])
def video1():
    return Response((genFrames()), mimetype='multipart/x-mixed-replace; boundary=frame')
@views.route('/video2', methods=['GET', 'POST'])
def video2():
    return Response((genFrames2()), mimetype='multipart/x-mixed-replace; boundary=frame')


# receive frames from
def genFrames():
    cursor1 = connectToDb()
    users = UsersGetting(cursor1)
    userids = users.gettingUserId()
    # cam = find_camera(camid)
    video_capture1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # video_capture2 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    try:
        while True:
            frame = mainWorking(video_capture1, 0, userids, cursor1)
            # frame2 = mainWorking(video_capture2, 1, userids, cursor1)
            ret, buffer = cv2.imencode('.jpg', frame)
            # ret2, buffer2 = cv2.imencode('.jpg', frame2)
            frame = buffer.tobytes()
            # frame2=buffer2.tobytes()
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
            # yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame2 + b'\r\n'

    except Exception as e:
        
        print(e)
# receive frames from
def genFrames2():
    cursor1 = connectToDb()
    users = UsersGetting(cursor1)
    userids = users.gettingUserId()
    # cam = find_camera(camid)
    # video_capture1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    video_capture2 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    try:
        while True:
            # frame = mainWorking(video_capture1, 0, userids, cursor1)
            frame2 = mainWorking(video_capture2, 1, userids, cursor1)
            # ret, buffer = cv2.imencode('.jpg', frame)
            ret2, buffer2 = cv2.imencode('.jpg', frame2)
            # frame = buffer.tobytes()
            frame2=buffer2.tobytes()
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame2 + b'\r\n'
            # yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame2 + b'\r\n'

    except Exception as e:
        
        print(e)
        

@views.route('/barchart2/<userid>/<sdate>',methods=['GET','POST'])
def barchart2(userid,sdate):
    print("Today:",sdate)
    users = UsersGetting(cursor)
    timespends=users.getSpecificDateTimespend(userid,sdate)
    print(timespends)
    timespend=np.zeros(3)
    for row in timespends:
        print(row.locId)
        timespend[row.locId-1]=row.timeSpend
    if len(timespend)<3:
        timespend.append(0)
    print("TimeSpends:",timespend)

    
    print('H:',userid)
    Location=['TucShop','Cafeteria','SportsArea']
    revenue=[65,59,46]
    # timespend=[30,24,56]
    ypos=np.arange(len(Location))
    fig,ax=plt.subplots(figsize=(4,4))
    ax.set_title("User Daily Record")
    # ax.legend()
    ax.set_xticks(ypos,Location)
    ax.set_xlabel('Locations')
    ax.set_ylabel('Time Spend(min)')
    ax.bar(ypos,timespend)
    canvas=FigureCanvas(fig)
    img=io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img,mimetype='img/png')




# predict next location
def predictNewLocation(userId):
    users= UsersGetting(cursor)
    userLocations=users.getUserLocationNameOrdered(userId)

    df = pd.DataFrame(userLocations)
    print(df.head())
    df = pd.DataFrame((np.reshape(userLocations, (df.shape[0], 3))), columns=['locid', 'locName', 'time'])
    df['time'] = df['time'].astype(float)
    # print(df['time'])
    X_train, X_test, y_train, y_test = train_test_split((df[['time']]), (df.locName), train_size=0.8)
    model = linear_model.LogisticRegression()
    model.fit(X=X_train, y=y_train)
    newLoc = model.predict(X_test)

    return newLoc