import face_recognition
import pickle
import os



# The training data would be all the face encodings from all the known images and the labels are their names
encodings = []
names = []

# Training directory

all_face_encodings={}

def trainingImages():
    train_dir = os.listdir('website/static/images')
# Loop through each person in the training directory
    for person in train_dir:
        pix = os.listdir("website/static/images/" + person)
        

        # Loop through each training image for the current person
        for person_img in pix:
            # flip the image
            
            # Get the face encodings for the face in each image file
            face = face_recognition.load_image_file("website/static/images/" + person + "/" + person_img)
            face_bounding_boxes = face_recognition.face_locations(face)

            #If training image contains exactly one face
            if len(face_bounding_boxes) == 1:
                face_enc = face_recognition.face_encodings(face)[0]
                # Add face encoding for current image with corresponding label (name) to the training data
                encodings.append(face_enc)
                names.append(person)
                all_face_encodings[str(person)]=face_recognition.face_encodings(face)[0]
                
                
            else:
                print(person + "/" + person_img + " was skipped and can't be used for training")
                pass
    print(names)
    saveEncodings()
            


def saveEncodings():
    with open('dataset_faces.dat', 'wb') as f:
        pickle.dump(all_face_encodings, f)
        print("done")

from PIL import Image
import os, sys

path = "website/static/images"
dirs = os.listdir( path )

def resize():

    train_dir = os.listdir('website/static/images')
# Loop through each person in the training directory
    for person in train_dir:
        pix = os.listdir("website/static/images/" + person)
        
        print(pix)
        # Loop through each training image for the current person
        id=0
        for person_img in pix:
            img=Image.open("website/static/images/" + person + "/" + person_img)
            img=img.resize((80,80))
            print(person_img)
            img.save("website/static/images/" +person+'/'+person+str(id)+'_resized.jpg')
            id+=1



    print('image resized')

# resize()
# trainingImages()

from datetime import datetime,date

# dates in string format

# d1=date.today()
# print(d1) 
# d2='10-07-2022'
# # convert string to date object
# d1 = datetime.strftime(datetime.now().date(), "%d-%m-%Y")
# d1=datetime.strptime(d1,"%d-%m-%Y")
# d2 = datetime.strptime(d2, "%d-%m-%Y")

# # difference between dates in timedelta
# delta = abs(d2 - d1).days
# print(f'Difference is {delta} days')