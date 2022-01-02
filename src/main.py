
from crdoperations import UsersGetting
from training import trainingImages
# from dataset import DatasetGenerator
from dbconnection import DbConnection
from CameraFile import FPS, CameraThread

# main area



if __name__=="__main__":
    # datbase connection
    conn=DbConnection()
    conn.connectToDb()
    # getting userIds
    users=UsersGetting(cursor)
    userids=users.gettingUserId()
    trainingImages()

    cursor=conn.getCursor()
                 
    CameraThread(userids,cursor)
   
