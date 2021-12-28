from threading import Thread
import threading
import time
import cv2


class WebCamStream:
    def __init__(self,src=0,name="Camera1") -> None:
        self.stream=cv2.VideoCapture(src)
        self.ret,self.frame=self.stream.read()
        self.name=name

        self.stopped=False


    def start(self):

        t=threading.Thread(target=self.update,name=self.name,args=())
        t.start()
        t.join()
        return self

    def update(self):
        try:

            while self.stream.isOpened():

                if self.stopped:
                    print("Stopping camera")
                    time.sleep(1)
                    self.stream.release()
                    break
                    
                    
                else:
                    print('a')
                    self.ret,self.frame=self.stream.read()
                    cv2.imshow(self.name,self.frame)
                    if cv2.waitKey(1) & 0xFF == ord('z'):
                        self.stop()
        except Exception as e:
            print(e)
    def resume(self,src):
        
        self.stopped=False
        self.stream=cv2.VideoCapture(src)

    def read(self):
        return self.frame
    
    def stop(self):
        self.stopped=True



