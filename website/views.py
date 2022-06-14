
from time import sleep, time
from cv2 import VideoCapture
from flask import Blueprint, redirect,render_template, request,flash,session,Response
from .import connectToDb
from .crdoperations import UsersGetting
import folium,cv2,os
from .CameraFile import cameraThread, mainWorking

# our db cursor
cursor=connectToDb()

views=Blueprint('views',__name__)

camerasList=[0,1]


def find_camera(list_id):
    return camerasList[int(list_id)]

# home page route
@views.route('/home')

def homePage():
    headings=(("id"),("Name"),("Image"))
    if 'userid' in session:
        cursor.execute("Select * from tbPerson")    
        personData=cursor.fetchall()
        print(personData)
        
        imagesPath=[]
        basePath='website/static/images'
        train_dir = os.listdir(basePath)
        for person in train_dir:
            pix = os.listdir("website/static/images/" + person)
            # for person_img in pix:
            
            imagesPath.append('images'+'/'+str(person)+'/'+pix[0])
            print(imagesPath)
        for i in range(len(personData)):
            personData[i][-1]=imagesPath[i]
            # print(os.path.join(str(pix),pix[0]))
        
        return render_template('home.html',headings=headings,data=personData)
    
    else:
        return redirect('/')


@views.route('/user/<user_id>')

def userDetail(user_id):
    print(user_id)
    users=UsersGetting(cursor)
    allRecords=users.getAllLocationRecord(user_id)
    map=folium.Map(location=[24.793864397827658, 67.1351927],min_zoom=18,zoom_start=18,height=350,width=600,min_lat=24.7,max_lat=24.8,min_lon=67,max_lon=67.15,left="20%",top="10%",zoom_control=False)
    for row in allRecords:
        print(row)
        
        tooltip=""
        folium.Marker([row[-2], row[-1]],popup="l",tooltip=tooltip).add_to(map)
        # generate map
        map.save("website/templates/map.html")

    return render_template("userdetail.html",uid=user_id,userLocationRecord=allRecords)

# for map


# route for login page
@views.route('/')

def login():
    return render_template('login.html')

# route for login post
@views.route('/login_validation',methods=['POST'])

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
@views.route('/signup')
def signup():
    return render_template('signup.html')

@views.route('/signup',methods=['POST'])
def signUser():
    email= request.form.get('email')
    password1=request.form.get('password1')
    password2=request.form.get('password2')
    message="Successfully Registered!"
    if password1==password2 :
        cursor.execute("insert into tbAdmins values(?,?)",email,password1)
        
        flash(message)
        (2)
        return redirect('/')

    else:
        message="Passwords Donot Match"
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
    return render_template('cameras.html',cameraList=camerasList)


@views.route('/video/<string:id>',methods=['GET','POST'])
def video(id):
    return Response(genFrames(id), mimetype='multipart/x-mixed-replace; boundary=frame')

def genFrames(camid):

    users=UsersGetting(cursor)
    userids=users.gettingUserId() 
    
    cam = find_camera(camid)

    video_capture = cv2.VideoCapture(cam,cv2.CAP_DSHOW)
    try:
        while(True):  

            frame=mainWorking(video_capture,cam,userids,cursor)
            ret, buffer = cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()
            yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except Exception as e:
        print(e)

# @views.route('/user/<user_id>',methods=['GET','POST'])
# def userDetail(user_id):
#     # print(user_id)
    
#     users = UsersGetting(cursor)
#     allRecords = users.getAllLocationRecord(user_id)
#     print(allRecords)
#     location = predictNewLocation(cursor, user_id)

#     currentDateRecords=users.getCurrentDateLocations(user_id)

#     map = folium.Map(location=[24.79387658, 67.1351927], max_zoom=18, zoom_start=12, height=300, width='60%', min_lat=24.6, max_lat=24.8, min_lon=66, max_lon=67.15, left='20%', top='5%', zoom_control=True)
#     for row in currentDateRecords:
#         # print(row)
#         # tooltip = str(row[1])
#         folium.Circle(location=[
#          row[-3], row[-2]],
#           radius=2,
#           popup=(str(row[0])),
#           color='#3186cc',
#           fill=True,
#           fill_color='#3186cc').add_to(map)
    
#     map.save('website/templates/map.html')

#     return render_template('userdetail.html', uid=user_id, userLocationRecord=allRecords, location=location)