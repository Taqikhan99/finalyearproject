import cv2
import cvzone

from cvzone.FaceMeshModule import FaceMeshDetector

# cap=cv2.VideoCapture(0)
# detector=FaceMeshDetector(maxFaces=1)



def findFacedistance(img):
    detector=FaceMeshDetector()
    img,faces=detector.findFaceMesh(img,draw=False)

    # We need to find the points of eyes
    if faces:
        # print(len(faces))
        for face in faces:
            # face=faces[0]
            pointLeft=tuple(face[145])
            pointRight=tuple(face[374])
            # cv2.circle(img,pointLeft,5,(200,0,0),cv2.FILLED)
            # cv2.circle(img,pointRight,5,(200,0,0),cv2.FILLED)
            # cv2.line(img,pointLeft,tuple(pointRight),(100,250,0),2)

            # Finding focal length f= w*d/W
            w,_=detector.findDistance(pointLeft,pointRight)
            W=6.3
            # d=50
            # # print(w)
            # f= (w*d)/W

            # print(f)
            f=600

            # Finding distance d=(W*f)/w
            d=(W*f)/w
            print(d/2.54)
            return round(d/2.54,1)
        # cvzone.putTextRect(img,f'Distance: {round(d/2.54,1)} inch',(face[10][0]-120,face[10][1]-100),scale=1.4,colorT=(244,0,0),colorR=(50,255,10))

# while True:
#     ret,img=cap.read()
#     img,faces=detector.findFaceMesh(img,draw=False)

#     # We need to find the points of eyes
#     if faces:
#         face=faces[0]
#         pointLeft=tuple(face[145])
#         pointRight=tuple(face[374])
#         # cv2.circle(img,pointLeft,5,(200,0,0),cv2.FILLED)
#         # cv2.circle(img,pointRight,5,(200,0,0),cv2.FILLED)
#         # cv2.line(img,pointLeft,tuple(pointRight),(100,250,0),2)

#         # Finding focal length f= w*d/W
#         w,_=detector.findDistance(pointLeft,pointRight)
#         W=6.3
#         # d=50
#         # # print(w)
#         # f= (w*d)/W

#         # print(f)
#         f=620

#         # Finding distance d=(W*f)/w
#         d=(W*f)/w
#         print(round(d/2.54,1))
#         cvzone.putTextRect(img,f'Distance: {round(d/2.54,1)} inch',(face[10][0]-120,face[10][1]-100),scale=1.4,colorT=(244,0,0),colorR=(50,255,10))

#     cv2.imshow("Image",img)
#     if cv2.waitKey(1) & 0xFF == ord('z'):
#                 break  