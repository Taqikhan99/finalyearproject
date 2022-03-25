from distutils.log import debug


from crdoperations import UsersGetting
from training import trainingImages

# from dataset import DatasetGenerator
from dbconnection import DbConnection
from CameraFile import cameraThread

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      


if __name__=="__main__":
    # datbase connection
    
    conn=DbConnection()
    conn.connectToDb() 
     
    
    trainingImages()
    cursor=conn.getCursor()
    # getting userIds
    users=UsersGetting(cursor)
    userids=users.gettingUserId() 
                 
    cameraThread(userids)
    

   
