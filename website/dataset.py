
import cv2,time,numpy as np
from pathlib import Path

class DatasetGenerator:

    imgid=1
    def convertToGray(self,img):

        gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
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
        Path("website/static/images/user_{}".format(userid)).mkdir(parents=True,exist_ok=True)
        
        try:
            img=self.convertToGray(img)    
            while self.imgid<=3:
                
                  
                img=self.resizeImg(img)
                flipImg=self.flipImg(img)
                sharpenedImg=self.sharpen(img)
                # shiftedImg=self.imgShift(img)

                savingPath="website/static/images/user_"+str(userid)+"/user_"+str(userid)+"."+str(self.imgid)+".jpg"
                savingFlippedPath="website/static/images/user_"+str(userid)+"/user_"+str(userid)+"_flip."+str(self.imgid)+".jpg"
                savingSharpendPath="website/static/images/user_"+str(userid)+"/user_"+str(userid)+"_sharpen."+str(self.imgid)+".jpg"
                # savingShiftedPath="images/user_"+str(userid)+"/user_"+str(userid)+"_shifted."+str(self.imgid)+".jpg"

                cv2.imwrite(savingPath,img)
                cv2.imwrite(savingFlippedPath,flipImg)
                cv2.imwrite(savingSharpendPath,sharpenedImg)
                # cv2.imwrite(savingShiftedPath,shiftedImg)
                self.imgid+=1
            
            print("Images saved!")
            
            # print("self.imgid: ",self.imgid)
            return self.imgid         
        except Exception as e:
            print('Check please ',e)
        