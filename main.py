import cv2
import threading
import face_recognition
import cv2,multiprocessing as mp,time
import numpy as np
import time,os,pickle
from crdoperations import UserIdsGetting
from training import names,encodings, trainingImages
# from dataset import DatasetGenerator
from dbconnection import DbConnection

from CameraFile import FPS, CameraThread, camThread,cameraSetup

# main area

if __name__=="__main__":
    # datbase connection
    conn=DbConnection()
    conn.connectToDb()
    print(mp.cpu_count())
    # getting userIds
    users=UserIdsGetting()
    userids=users.gettingUserId(conn.cursor)
    # making fps obj
    trainingImages()

    cursor=conn.getCursor()
    
    # thread2.join()
                 
    CameraThread(userids,cursor)
   
