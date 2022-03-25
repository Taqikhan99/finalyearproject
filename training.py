import face_recognition
import pickle
import os,cv2

# Training the SVC classifier

# The training data would be all the face encodings from all the known images and the labels are their names
encodings = []
names = []

# Training directory

all_face_encodings={}

def trainingImages():
    train_dir = os.listdir('static/images')
# Loop through each person in the training directory
    for person in train_dir:
        pix = os.listdir("static/images/" + person)
        

        # Loop through each training image for the current person
        for person_img in pix:
            # flip the image
            
            # Get the face encodings for the face in each image file
            face = face_recognition.load_image_file("static/images/" + person + "/" + person_img)
            face_bounding_boxes = face_recognition.face_locations(face)

            #If training image contains exactly one face
            if len(face_bounding_boxes) == 1:
                face_enc = face_recognition.face_encodings(face)[0]
                # Add face encoding for current image with corresponding label (name) to the training data
                encodings.append(face_enc)
                names.append(person)
                all_face_encodings[str(person)]=face_recognition.face_encodings(face)[0]
            else:
                # print(person + "/" + person_img + " was skipped and can't be used for training")
                pass
    print(names)
        
# trainingImages()

def saveEncodings():
    with open('dataset_faces.dat', 'wb') as f:
        pickle.dump(all_face_encodings, f)