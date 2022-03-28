from threading import Thread
import cv2
import numpy as np

from dbconnection import DbConnection
from test2 import face_data2
from training import trainingImages

from dataset import DatasetGenerator
from recognition import recognize
from crdoperations import UserInsertion,UsersGetting, calcTimeDifference
from geopy.distance import distance,Distance
# from faceDistance import findDistance

# Initialize some variables
class CameraThreadInitializer(Thread):

    def __init__(self, previewName,camID,userids):

        dbConnection=DbConnection()
        dbConnection.connectToDb()

        Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
        self.userids=userids
        self.cursor=dbConnection.getCursor()

    def run(self):

        print ("Starting " + self.previewName)
        mainWorking(self.previewName,self.camID,self.userids,self.cursor)


# starting cameras here
def cameraThread(camName,camid,userids):
    
    thread=CameraThreadInitializer(camName,camid,userids)
    # thread2=CameraThreadInitializer("camera 2",2,userids)
    
    
    thread.start()
    # thread2.start()
    
    

def mainWorking(camNam,camId,userids,cursor):

    # initialize object for get operations
    users=UsersGetting(cursor)
     # initialize object for insert operations
    userInsertObj=UserInsertion(cursor)
    generator=DatasetGenerator()
    # image id at start
    imgid=1
    # setting cameraId
    cameraLocId=camId+1
    savedUserIds=userids
    # starting camera read
    video_capture = cv2.VideoCapture(camId)
    
    try:
        while video_capture.isOpened():
            
            # Grab a single frame of video
            ret, frame = video_capture.read()
            
            userImg,idReturned,frame=recognize(frame,savedUserIds)
            print("id: ",idReturned)
            # getLastLoc
            userLastLocation=users.getLastLocationId(idReturned)
            userLastTime=users.getUserLastLocTime(idReturned)

            # get camera lat long
            latitude,longitude=users.getLatLong(locationId=cameraLocId)
            
            # check if id returned doesnot match with records
            
            if(idReturned>0 and idReturned not in savedUserIds):
                
                imgid=generator.generateDataset(userImg,idReturned)
                               
                if imgid>3:
                    
                    savedUserIds.append(idReturned)
                    # retrain the data
                    trainingImages()
                    generator.imgid=1
                    userInsertObj.insertUser(idReturned)
                    print("Saved user to database")       
            elif idReturned==0:
                pass
            else:
                # get distance to person face from camera (2.2672 is focal length in feet)
                distance=face_data2(frame,2.2672)
                
                # calculate user lat long by passing distance anc camera lat long
                 
                lat,long=getUserLatLong(distance,latitude,longitude)
                # cv2.putText(frame, str(lat)+str(long), ( 10,15), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

                minDifference=0
                if userLastTime is not None:
                    minDifference=calcTimeDifference(userLastTime)

                if userLastLocation !=cameraLocId or minDifference>5:
                    userInsertObj.insertUserLoc(idReturned,cameraLocId,lat,long)
                    # print("Location Saved")
                else:
                    print('user already at same location')
                    # findDistance(frame)

            cv2.imshow(camNam, frame)
            # Hit 'z' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('z'):
                break   
    except Exception as e:
        print(e) 
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()




def getUserLatLong(dist,lat,long):
    latlong=distance(feet=dist).destination((lat,long),bearing=180)
    latlong=latlong.format_decimal()
    latlong=str(latlong)
    latlong=latlong.split(',')

    lat=latlong[0]
    long=latlong[1]

    return lat,long







