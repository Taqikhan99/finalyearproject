
from crdoperations import UsersGetting
from training import trainingImages

# from dataset import DatasetGenerator
from dbconnection import DbConnection
from CameraFile import cameraThread
                                                                                                                                             
if __name__=="__main__":
    # datbase connection
    trainingImages()
    conn=DbConnection()
    conn.connectToDb() 
 
    cursor=conn.getCursor()
    # getting userIds
    users=UsersGetting(cursor)
    userids=users.gettingUserId() 
                 
    cameraThread("cam1",0,userids)
    # cameraThread("cam2",1,userids)
    

   
