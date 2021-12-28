import threading
import face_recognition
import cv2,multiprocessing as mp,time
import numpy as np
import time,os,pickle

from pathlib import Path
from crdoperations import UserIdsGetting
from recognition import  recognize
from  test4 import WebCamStream

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



def cameraSetup(camNam,camId,fpsObject,userInsertObj,names,encodings,userids,cursor):
    count=1
    cap = cv2.VideoCapture(camId)
    process_this_frame = True
    
    flag=True
    
    
    while cap.isOpened():
        

    # while video_capture.isOpened():
        
    #     # Grab a single frame of video
    #     ret, frame = video_capture.read()
    #     # fps=fpsObject.fpsCalculate()
        
    #     # Only process every other frame of video to save time
    #     if process_this_frame:
    #         count = 0
    #         frame=recognize(frame,userids[count + 1],userInsertObj,names,encodings,(255,0,0),cursor)
        
                
        
    #     # cv2.putText(frame,fps, (7, 70),cv2.FONT_HERSHEY_COMPLEX,1, (100, 255, 0),2, cv2.LINE_AA)    
    #     # Display the resulting image
    #     cv2.imshow(camNam, frame)

         

    #     # Hit 'q' on the keyboard to quit!
    #     if cv2.waitKey(1) & 0xFF == ord('z'):
    #         break
    
    
    # # Release handle to the webcam
    # video_capture.release()
    # cv2.destroyAllWindows()