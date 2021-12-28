import threading
import face_recognition
import cv2,multiprocessing as mp,time
import numpy as np
import time,os,pickle
from dataset import DatasetGenerator
from pathlib import Path
from crdoperations import UserIdsGetting
from recognition import  recognize
from training import trainingImages,names,encodings
from crdoperations import UserInsertion

# Initialize some variables
class camThread(threading.Thread):
    def __init__(self, previewName,camID, fpsObject,userids,cursor):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
        self.fpsObject=fpsObject
       
        self.userids=userids
        self.cursor=cursor
    def run(self):
        print ("Starting " + self.previewName)
        cameraSetup(self.previewName,self.camID,self.fpsObject,self.userids,self.cursor)

def CameraThread(userids,cursor):
    fpsObject=FPS()
    thread1=camThread("camera 1",1,fpsObject,userids,cursor)
    # thread2=camThread("camera 2",1,fpsObject,userInsertObj,names,encodings,userids)
    thread1.start()
    thread1.join()





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



generator=DatasetGenerator()
def cameraSetup(camNam,camId,fpsObject,userids,cursor):

    # starting camera read
    video_capture = cv2.VideoCapture(camId)
  
    userInsertObj=UserInsertion()
    imgid=1
    savedUserIds=userids

    while video_capture.isOpened():
        
        # Grab a single frame of video
        ret, frame = video_capture.read()
        # fps=fpsObject.fpsCalculate()
        
        userImg,idReturned,frame=recognize(frame,savedUserIds,names,encodings,cursor)
        
        if(idReturned not in savedUserIds):
            
            print(idReturned)
            imgid=generator.generateDataset(userImg,idReturned)
            if imgid==10:
                
                savedUserIds.append(idReturned)
                print(savedUserIds)
                # set imgid to 1 again
                generator.imgid=1
                # userInsertObj.insertUser(cursor,idReturned)
                # print("Saved user to database")
                # call training func
                trainingImages()
                time.sleep(0.5)
        else:

            print(idReturned)
            print("User Matched!")
                
        
        # cv2.putText(frame,fps, (7, 70),cv2.FONT_HERSHEY_COMPLEX,1, (100, 255, 0),2, cv2.LINE_AA)    
        # Display the resulting image
        cv2.imshow(camNam, frame)

         

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('z'):
            break
    
    
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

