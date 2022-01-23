from threading import Thread
import cv2
import numpy as np
import time,os,pickle
from dbconnection import DbConnection
from training import trainingImages
from dataset import DatasetGenerator
from recognition import  recognize
from crdoperations import UserInsertion,UsersGetting
import logging

# Initialize some variables
class CameraThreadInitializer(Thread):

    def __init__(self, previewName,camID,userids,cursor):

        dbConnection=DbConnection()
        dbConnection.connectToDb()

        Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
        self.userids=userids
        self.cursor=dbConnection.getCursor()

    def run(self):

        print ("Starting " + self.previewName)
        cameraSetup(self.previewName,self.camID,self.userids,self.cursor)


# starting cameras here
def cameraThread(userids,cursor):
    
    thread1=CameraThreadInitializer("camera 1",0,userids,cursor)
    thread2=CameraThreadInitializer("camera 2",1,userids,cursor)
    
    thread2.start()
    thread1.start()
    
    thread1.join()
    thread2.join()

def cameraSetup(camNam,camId,userids,cursor):

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

            # getLastLoc
            userLastLocation=users.getLastLocationId(idReturned)
            print(userLastLocation)
            # check if id returned doesnot match with records
            # for idReturned in idsReturned:
            if(idReturned>0 and idReturned not in savedUserIds):
                
                imgid=generator.generateDataset(userImg,idReturned)
                if imgid==10:
                    
                    savedUserIds.append(idReturned)
                    # retrain the data
                    trainingImages()
                    generator.imgid=1
                    userInsertObj.insertUser(idReturned)
                    print("Saved user to database")       
            elif idReturned==0:
                pass
            else:
                # print("User Matched!")
                # print (idReturned)
                
                # calling insert location query after some interval
                if userLastLocation !=cameraLocId:
                    userInsertObj.insertUserLoc(idReturned,cameraLocId)
                    # print("Location Saved")
                else:
                    print('user already at same location')

            cv2.imshow(camNam, frame)
            # Hit 'z' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('z'):
                break   
    except Exception as e:
        print(e) 
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()


class FPS:
    prevTime=0
    newTime=0
    
    def fpsCalculate(self):
        fps=0
        try:
            newTime=time.time()
            fps=1/(newTime-self.prevTime)
            FPS.prevTime=newTime
            fps=str(int(fps))
        except Exception as e:
            print(str(e))
        return fps