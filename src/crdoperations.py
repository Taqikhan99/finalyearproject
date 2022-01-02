
from time import strftime
import time
from dbconnection import DbConnection
from datetime import datetime 


# getting database cursor for query execution
class CursorGet:
    def __init__(self) -> None:
        self.cursor=None
    def setCursor(self,conn):
        self.cursor=conn.getCursor()
    def getCursor(self):
        return self.cursor

# getting all user records
class UsersGetting:
    def __init__(self,cursor) -> None:
        self.cursor=cursor
    def getAllUsers(self,cursor):
        
        self.cursor.execute("Select * from tbPerson")
        personData=cursor.fetchall()
        print(personData)
        return personData

    
    userIds=[]

    def gettingUserId(self):

        users=UsersGetting()    
        userdata=users.getAllUsers(self.cursor)
        for row in range(len(userdata)):
            # personIds.append(row[0])
            # personNames.append(row[1])
            self.userIds.append( userdata[row][0])
        return self.userIds

    def getUserLocations(self):
        
        self.cursor.execute('Select locId,personId from tbPersonLocation')
        personLocs=self.cursor.fetchall()
        return personLocs

    def getUserLocationsById(self,userId):
        self.cursor.execute(f'select distinct locid,Max(time) from tbPersonLocation where personId=${userId} Group by locId order by Max(time) desc,locId')

# insert new user in database

class UserInsertion:
 
    def insertUser(self,cursor,user_id):
        try:

                cursor.execute('''
                        INSERT INTO tbPerson (personId, pName, imagesPath)
                        VALUES
                        (?,?,?)
                        
                        ''',user_id,'user_'+str(user_id),'images/user_'+str(user_id))
                cursor.commit()
                
                print('Saved to database')
        except:
            print('Already saved for this user')
    
    def insertUserLoc(self,cursor,user_id,locId):
        cursor=cursor
        # if(UserInsertion.run==0):
            # currentTime=datetime.datetime.now()
        
        now = datetime.now()
        print('Now =: ',now)
        currentTime=now.strftime("%H:%M:%S")

    
        cursor.execute('''
                insert into tbPersonLocation(locId,personId,time)
                Values
                (?,?,?)
        ''',(locId,user_id,currentTime))
        cursor.commit()
        # cursor.close()
        print('location added!')

           