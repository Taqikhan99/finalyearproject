import cv2,time,numpy as np
from pathlib import Path

class DatasetGenerator:

    imgid=1
    def convertToGray(self,img):
        
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # gray=self.resizeImg(gray)
        return gray

    def resizeImg(self,img):

        resize=cv2.resize(img,(150,150))
        return resize

    def flipImg(self,img):

        flip=cv2.flip(img,1)
        return flip

    def sharpen(self,img):

        kernel = np.array([[-1, -1, -1],
                   [-1, 10,-1],
                   [-1, -1, -1]])
        image_sharp = cv2.filter2D(src=img, ddepth=-1, kernel=kernel)
        return image_sharp

    def imgShift(self,img):
        
        matrix=np.float32([[1,0,20],[0,1,50]])
        translated=cv2.warpAffine(img,matrix,img.shape)
        return translated
        
    def generateDataset(self,img, userid):
        
        # creating a folder for a user
        Path("static/images/user_{}".format(userid)).mkdir(parents=True,exist_ok=True)
        
        try:
            time.sleep(0.025)    
            if self.imgid<=3:

                img=self.convertToGray(img)   
                img=self.resizeImg(img)
                flipImg=self.flipImg(img)
                sharpenedImg=self.sharpen(img)
                # shiftedImg=self.imgShift(img)

                savingPath="static/images/user_"+str(userid)+"/user_"+str(userid)+"."+str(self.imgid)+".jpg"
                savingFlippedPath="static/images/user_"+str(userid)+"/user_"+str(userid)+"_flip."+str(self.imgid)+".jpg"
                savingSharpendPath="static/images/user_"+str(userid)+"/user_"+str(userid)+"_sharpen."+str(self.imgid)+".jpg"
                # savingShiftedPath="images/user_"+str(userid)+"/user_"+str(userid)+"_shifted."+str(self.imgid)+".jpg"

                cv2.imwrite(savingPath,img)
                cv2.imwrite(savingFlippedPath,flipImg)
                cv2.imwrite(savingSharpendPath,sharpenedImg)
                # cv2.imwrite(savingShiftedPath,shiftedImg)
            else:
                print("Images saved!")
            self.imgid+=1
            return self.imgid         
        except Exception as e:
            print('Check please ',e)
        