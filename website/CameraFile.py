from threading import Thread
from time import sleep
import cv2
import numpy as np
from datetime import datetime
from .dbConnection import DbConnection
from .distanceWorking import face_data2,face_data3
from .training import trainingImages

# from face_recognition.api import face_locations
# from .training import names,encodings
import face_recognition,pickle
# from faceDistance import findFacedistance
from .distanceWorking import face_data3
from .dataset import DatasetGenerator
# from .recognition import recognize
from .crudOperations import UserInsertion,UsersGetting
from geopy.distance import distance,Distance
# from faceDistance import findDistance

with open('dataset_faces.dat', 'rb') as f:
	all_face_encodings = pickle.load(f)
names=list(all_face_encodings.keys())
encodings = np.array(list(all_face_encodings.values()))
    

class CameraWork:    
    def __init__(self,video_capture,cameraLocId,userids,cursor):
        self.videocapture=video_capture
        
        self.saveduserids=userids
        self.cursor=cursor
        self.cameraLocId=cameraLocId



    # For main entrance camera
    # -----------------------------------

    def mainWorking(self):
    # initialize object for get operations
        users=UsersGetting(self.cursor)
        # initialize object for insert operations
        userInsertObj=UserInsertion(self.cursor)
        generator=DatasetGenerator()
        # image id at start
        imgid=1
        
        
        
        # get camera lat long
        latitude,longitude=users.getLatLong(locationId=self.cameraLocId)
        
        try:
            while self.videocapture.isOpened():
                
                # Grab a single frame of video
                sucess, frame = self.videocapture.read()
                
                userImg,idReturned,frame,distance=self.recognize(frame,self.saveduserids)
               
                userLastLocation=users.getLastLocationId(idReturned)
            
                userLastTime=users.getUserLastLocTime(idReturned)
                # print(userLastTime)
                timeDiff=calcTimeDifference(userLastTime)
                
                
                # check if id returned doesnot match with records
                
                if(idReturned>0 and idReturned not in self.saveduserids):
                    imgid=generator.generateDataset(userImg,idReturned)
                    print("Image id: ",imgid)            
                    if imgid>2:
                        
                        self.saveduserids.append(idReturned)
                        # retrain the data
                        trainingImages()
                        generator.imgid=1
                        userInsertObj.insertUser(idReturned)
                        print("Saved user to database")
                   
                elif idReturned==0:
                    pass
                else:
                    
                    lat,long=getUserLatLong(distance,latitude,longitude)
                    
                    #insert userlocation every minute or when location changes
                    if userLastLocation !=self.cameraLocId :
                        userInsertObj.insertUserLoc(idReturned,self.cameraLocId,lat,long)
                        
                    else:
                        print('user already at same location')
                
                return frame
            
        except Exception as e:
            print("Some error1: ",e)



    # For other inside building cameras
    # --------------------------------------

    def mainWorking2(self):
    # initialize object for get operations
        users=UsersGetting(self.cursor)
        # initialize object for insert operations
        userInsertObj=UserInsertion(self.cursor)
        generator=DatasetGenerator()
        # image id at start
        imgid=1
        
        
        
        # get camera lat long
        latitude,longitude=users.getLatLong(locationId=self.cameraLocId)
        
        try:
            while self.videocapture.isOpened():
                
                # Grab a single frame of video
                sucess, frame = self.videocapture.read()
                
                userImg,idReturned,frame,distance=self.recognize(frame,self.saveduserids)
               
                userLastLocation=users.getLastLocationId(idReturned)
            
                userLastTime=users.getUserLastLocTime(idReturned)
                # print(userLastTime)
                timeDiff=calcTimeDifference(userLastTime)
                
                
                # check if id returned doesnot match with records
                
                if(idReturned>0 and idReturned not in self.saveduserids):
                    pass
                    
                elif idReturned==0:
                    pass
                else:
                    
                    #insert userlocation  when location changes
                    if userLastLocation !=self.cameraLocId :
                        lat,long=getUserLatLong(distance,latitude,longitude)
                        userInsertObj.insertUserLoc(idReturned,self.cameraLocId,lat,long)
                        
                    else:
                        pass
                        # print('user already at same location')
                        
                
                
                return frame
            
        except Exception as e:
            print("Some error: ",e) 



    # For user path prediction
    def modelTraining(self,userid):
        # initialize object for get operations
        users=UsersGetting(self.cursor)
        users.getUserAllLocations()

    
    
    def recognize(self,frame,userids):
    
        distance=0
        
        userImg=0
        newuserId=0

        processFrame=True

        if processFrame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
            
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame,number_of_times_to_upsample=3,model="cnn")
            
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations,num_jitters=3)
            # print(len(face_locations))
            
            face_names = []
            try: 
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    
                    matches = face_recognition.compare_faces(encodings, face_encoding,tolerance=0.6)
                    name = "unknown"
                    face_distances = face_recognition.face_distance(encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    # matchPercent=(1-face_distances[best_match_index])*100
                    # print(round(matchPercent,2))
                    if matches[best_match_index]:
                        name = names[best_match_index]
                        newuserId=int(name.split("_")[1])
                        
                    face_names.append(name)
                    

            except Exception as e:
                print(e)
            
            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                
                
                # Draw a label with a name above the face
                cv2.rectangle(frame, (left, top-25), (right,top-10), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, top-15), font, 0.5, (255, 255, 255), 1)

                # calc distance
                distance=face_data3(frame,2.2672,right-left)
                cv2.putText(
                frame, f"Dist = {round(distance,1)} ft", (left+10, top-40), font, 0.6, (255, 255, 255), 1)
            
                if name=="unknown":
                    newuserId=userids[-1]+1
                    print(newuserId)
                    cv2.putText(frame, name, (left + 6, top-15), font, 0.5, (255, 255, 255), 1)
                    cv2.rectangle(frame, (left-10, top-10), (right+10, bottom+10), (0, 0, 255), 1)
                    
                    userImg=frame[top-10:bottom+10,left-5:right+5]

                else:

                    cv2.rectangle(frame, (left-1, top), (right+1, bottom), (0, 255, 0), 1)
                    
                
        
        return userImg,newuserId,frame,distance



    
# calculate lat long

def getUserLatLong(dist,lat,long):
    latlong=distance(feet=dist).destination((lat,long),bearing=180)
    latlong=latlong.format_decimal()
    latlong=str(latlong)
    latlong=latlong.split(',')

    lat=latlong[0]
    long=latlong[1]

    return lat,long



# calculate time difference
def calcTimeDifference(timeDate):
    tdMins=0
    try:
        fmt = '%d-%m-%y %H:%M:%S'
        tstamp1 = datetime.strptime(timeDate, fmt)
        tstamp2 = datetime.now().strftime("%d-%m-%y %H:%M:%S")
        tstamp2 =datetime.strptime(tstamp2,fmt)
        # print(tstamp1," | ",tstamp2) 
        elapsedTime=tstamp2-tstamp1
        
        if int(elapsedTime.total_seconds()%60)>=1:
            tdMins=int(elapsedTime.total_seconds()/60)
        print("mins: ",int(elapsedTime.total_seconds()/60))
    except:
        pass
    return tdMins





    
