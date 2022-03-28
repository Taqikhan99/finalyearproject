import cv2

# variables
# distance from camera to object(face) measured
# KNOWN_DISTANCE = 70  # centimeter
KNOWN_DISTANCE = 2.6  # ft
# width of face in the real world or Object Plane
#KNOWN_WIDTH = 14.3  # centimeter
KNOWN_WIDTH = 0.5  # ft
# Colors
GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
fonts = cv2.FONT_HERSHEY_COMPLEX
cap = cv2.VideoCapture(0)

# face detector object
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


# focal length finder function
def focal_length(measured_distance, real_width, width_in_rf_image):
    """
    This Function Calculate the Focal Length(distance between lens to CMOS sensor), it is simple constant we can find by using
    MEASURED_DISTACE, REAL_WIDTH(Actual width of object) and WIDTH_OF_OBJECT_IN_IMAGE
    :param1 Measure_Distance(int): It is distance measured from object to the Camera while Capturing Reference image
    :param2 Real_Width(int): It is Actual width of object, in real world (like My face width is = 14.3 centimeters)
    :param3 Width_In_Image(int): It is object width in the frame /image in our case in the reference image(found by Face detector)
    :retrun focal_length(Float):"""
    print("mdist: ",measured_distance)
    print("mWidth: ",width_in_rf_image)
    print("RWidth: ",real_width)
    focal_length_value = (width_in_rf_image * measured_distance) / real_width
    print(focal_length_value)
    return focal_length_value


# distance estimation function
def distance_finder(focal_length, real_face_width, face_width_in_frame):
    """
    This Function simply Estimates the distance between object and camera using arguments(focal_length, Actual_object_width, Object_width_in_the_image)
    :param1 focal_length(float): return by the focal_length_Finder function
    :param2 Real_Width(int): It is Actual width of object, in real world (like My face width is = 5.7 Inches)
    :param3 object_Width_Frame(int): width of object in the image(frame in our case, using Video feed)
    :return Distance(float) : distance Estimated
    """
    distance = (real_face_width * focal_length) / face_width_in_frame
    return distance


# face detector function
def face_data(image):
    """
    This function Detect the face
    :param Takes image as argument.
    :returns face_width in the pixels
    """

    face_width = 0
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray_image, 1.3, 10)
    for (x, y, h, w) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), WHITE, 1)
        face_width = w
        print(face_width)
        

    return face_width

def face_data2(image,focalLength):
    face_width = 0
    distance=0
    # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray_image=
    faces = face_detector.detectMultiScale(image, 1.3, 10)
    for (x, y, h, w) in faces:
        # cv2.rectangle(image, (x, y), (x + w, y + h), WHITE, 1)
        face_width = w/305
        
        distance=distance_finder(focalLength, KNOWN_WIDTH, face_width)
        
        cv2.putText(
            image, f"Dist = {round(distance,1)} ft", (x+10, y-20), fonts, 0.6, (WHITE), 1)
    
    return distance

# reading reference image from directory
# ref_image = cv2.imread("testimage.jpg")

# # ref_image=cv2.resize(ref_image,(300,300))
# ref_image_face_width = face_data(ref_image)
# focal_length_found = focal_length(KNOWN_DISTANCE, KNOWN_WIDTH, 0.436)
# print(focal_length_found)
# # cv2.imshow("ref_image", ref_image)

# while True:
#     _, frame = cap.read()
     
#     # calling face_data function
#     face_width_in_frame,Distance = face_data2(frame,focal_length_found)
#     # finding the distance by calling function Distance
    
        
#     cv2.imshow("frame", frame)
#     if cv2.waitKey(10) == ord("q"):
#         break
# cap.release()
# cv2.destroyAllWindows()