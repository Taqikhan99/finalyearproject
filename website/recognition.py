from turtle import distance
import cv2,numpy as np
# from face_recognition.api import face_locations
from .training import names,encodings
import face_recognition,pickle
# from faceDistance import findFacedistance


# with open('dataset_faces.dat', 'rb') as f:
# 	all_face_encodings = pickle.load(f)
# names=list(all_face_encodings.keys())
# encodings = np.array(list(all_face_encodings.values()))    

def recognize(frame,userids):
    
    
    userImg=0
    userId=0  
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
     
    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame,number_of_times_to_upsample=3,model="hog")
    
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
            matchPercent=(1-face_distances[best_match_index])*100
            print(round(matchPercent,2))
            
            if matches[best_match_index]:
                name = names[best_match_index]
                userId=int(name.split("_")[1])
                
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
        if name=="unknown":
            userId=userids[-1]+1
            
            cv2.putText(frame, name, (left + 6, top-15), font, 0.5, (255, 255, 255), 1)
            cv2.rectangle(frame, (left-10, top-10), (right+10, bottom+10), (0, 0, 255), 1)
            
            userImg=frame[top-10:bottom+10,left-5:right+5]

        else:
            
            
            cv2.rectangle(frame, (left-1, top), (right+1, bottom), (0, 255, 0), 1)
            
                         
            
    # return userImg,userId,frame
    return userImg,userId,frame
    



