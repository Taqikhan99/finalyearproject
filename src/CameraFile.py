import threading
import cv2
import numpy as np
import time,os,pickle
from training import trainingImages
from dataset import DatasetGenerator
from recognition import  recognize
from crdoperations import UserInsertion,UsersGetting


# Initialize some variables
class camThread(threading.Thread):
    def __init__(self, previewName,camID,userids,cursor):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
        self.userids=userids
        self.cursor=cursor
    def run(self):
        print ("Starting " + self.previewName)
        cameraSetup(self.previewName,self.camID,self.userids,self.cursor)


# starting cameras here
def CameraThread(userids,cursor):
    # fpsObject=FPS()
    thread1=camThread("camera 2",0,userids,cursor)
    # thread2=camThread("camera 1",0,fpsObject,userids,cursor)
    # thread2=camThread("camera 2",1,fpsObject,userInsertObj,names,encodings,userids)
    thread1.start()
    # thread2.start()
    thread1.join()
    # thread2.join()



def cameraSetup(camNam,camId,userids,cursor):
    users=UsersGetting(cursor)
    userInsertObj=UserInsertion(cursor)
    generator=DatasetGenerator()
    imgid=1

    # setting cameraId
    cameraLocId=camId+1
    savedUserIds=userids
    # starting camera read
    video_capture = cv2.VideoCapture(camId)
    

    while video_capture.isOpened():
        
        # Grab a single frame of video
        ret, frame = video_capture.read()

        userImg,idReturned,frame=recognize(frame,savedUserIds)

        # getLastLoc
        userLastLocation=users.getLastLocationId(idReturned)
        print(userLastLocation)
        # check if id returned doesnot match with records
        # for idReturned in idsReturned:
        if(idReturned not in savedUserIds):
            
            imgid=generator.generateDataset(userImg,idReturned)
            if imgid==10:
                
                savedUserIds.append(idReturned)
                # retrain the data
                trainingImages()
                time.sleep(0.1)
                generator.imgid=1
                userInsertObj.insertUser(idReturned)
                print("Saved user to database")       
        elif idReturned==0:
            pass
        else:
            print("User Matched!")
            print (idReturned)
            
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