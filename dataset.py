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
            if DatasetGenerator.imgid<=5:    
                img=self.resizeImg(img)
                savingPath="images/user_"+str(userid)+"/user_"+str(userid)+"."+str(DatasetGenerator.imgid)+".jpg"
                
                cv2.imwrite(savingPath,img)
            else:
                print("Images saved!")
            DatasetGenerator.imgid+=1 
                 
        except:
            print('Check please')