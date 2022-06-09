

from time import strftime
import time
from .dbconnection import DbConnection
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
    userIds=[]
    
    def __init__(self,cursor) -> None:
        self.cursor=cursor
    def getAllUsers(self):
        
        self.cursor.execute("Select * from tbPerson")
        personData=self.cursor.fetchall()
        print(personData)
        return personData

    
    

    def gettingUserId(self):
    
        userdata=self.getAllUsers()
        for row in range(len(userdata)):
           
            self.userIds.append( userdata[row][0])
        return self.userIds


    def getAllLocationRecord(self,userid):
        self.cursor.execute('Select * from tbPersonLocation where personId=?',userid)
        personLocs=self.cursor.fetchall()
        return personLocs

    def getUserLocations(self):
        
        self.cursor.execute('Select locId,personId from tbPersonLocation')
        personLocs=self.cursor.fetchall()
        return personLocs

    def getUserLocationsById(self,userId):
        
        self.cursor.execute('select distinct locid,Max(time) from tbPersonLocation where personId=?',userId,' Group by locId order by Max(time) desc,locId')
        personLoc=self.cursor.fetchall()
        
        return personLoc

    def getLastLocationId(self,userId):
        try:
            self.cursor.execute('select top 1 locId from tbPersonLocation where personId= ? order by date,time desc',userId)
            rows=self.cursor.fetchall()
            for row in rows:
                return row.locId
        except Exception as e:
            print('Error: ',e)

    def getUserLastLocTime(self,userId):
        try:
            self.cursor.execute('select top 1 date,time from tbPersonLocation where personId= ? order by time desc',userId)
            rows=self.cursor.fetchall()
            for row in rows:
                date=row.date
                time=row.time
                uDateTime=date+" "+time
                return uDateTime
        except Exception as e:
            print('Error: ',e)


    def getUserLocationNames(self,userId):
        userLocations=[]
        try:
            self.cursor.execute('''select tbLocation.locName from tbLocation
                                    inner join tbPersonLocation
                                    on tbLocation.locId=tbPersonLocation.locId
                                    where tbPersonLocation.personId=?''',userId)
            rows=self.cursor.fetchall()
            for row in rows:
                userLocations.append(row.locName)
            return userLocations
        except Exception as e:
            print('error1:',e)



        # get lat long of areaLocation
    def getLatLong(self,locationId):

        self.cursor.execute("select latitude,longitude from tbLocation where tbLocation.locId=?",locationId)
        data=self.cursor.fetchall()
     
        lat=data[0][0]
        long=data[0][1]
        long=float(long)
        
        lat=float(lat)
        
        
        return lat,long


# insert new user in database

class UserInsertion:
    def __init__(self,cursor) -> None:
        self.cursor=cursor
    def insertUser(self,user_id):
        try:

                self.cursor.execute('''
                        INSERT INTO tbPerson (personId, pName, imagesPath)
                        VALUES
                        (?,?,?)
                        
                        ''',user_id,'user_'+str(user_id),'static/images/user_'+str(user_id))
                self.cursor.commit()
                
                print('Saved to database')
        except:
            print('Already saved for this user')
    
    def insertUserLoc(self,user_id,locId,lat,long):
        
        now = datetime.now()
        
        currentTime=now.strftime("%H:%M:%S")
        currentDate= now.strftime("%d-%m-%y") 
        print(currentDate)
    
        self.cursor.execute('''
                insert into tbPersonLocation(locId,personId,date,time,latitude,longitude)
                Values
                (?,?,?,?,?,?)
        ''',(locId,user_id,currentDate,currentTime,lat,long))
        
        self.cursor.commit()
        # cursor.close()

def calcTimeDifference(timeDate):
    fmt = '%d-%m-%y %H:%M:%S'
    tstamp1 = datetime.strptime(timeDate, fmt)
    tstamp2 = datetime.now().strftime("%d-%m-%y %H:%M:%S")
    tstamp2 =datetime.strptime(tstamp2,fmt)
     
    elapsedTime=tstamp2-tstamp1
    
    tdMins=int(round(elapsedTime.total_seconds()/60))
    return tdMins


# conn=DbConnection()
# conn.connectToDb() 
# cursor=conn.getCursor()       
# users=UsersGetting(cursor)
# uDate,uTime=users.getUserLastLocTime(5)
# uDateTime=uDate+" "+uTime
# print(uDateTime)
# calcTimeDifference(uDateTime)







 
