import cv2,time
from pathlib import Path

class DatasetGenerator:
    imgid=1
    def convertToGray(self,img):
        # convert to gray and resize before saving
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        gray=self.resizeImg(gray)
        return gray
    def resizeImg(self,img):
        resize=cv2.resize(img,(200,200))
        return resize
    def generateDataset(self,img, userid):

        # creating a folder for a user
        Path("images/user_{}".format(userid)).mkdir(parents=True,exist_ok=True)
        # gray=self.convertToGray(img)
        # writing images in the user folder
        try:
            time.sleep(0.1)    
            if self.imgid<=10: 
                # img=self.convertToGray(img)   
                img=self.resizeImg(img)
                savingPath="images/user_"+str(userid)+"/user_"+str(userid)+"."+str(self.imgid)+".jpg"
                
                cv2.imwrite(savingPath,img)
            else:
                print("Images saved!")
            self.imgid+=1
            return self.imgid         
        except Exception as e:
            print('Check please ',e)
        