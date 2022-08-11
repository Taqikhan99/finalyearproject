

from time import strftime
import time
from .dbConnection import DbConnection
from datetime import datetime


# getting database cursor for query execution
class CursorGet:
    def __init__(self) -> None:
        self.cursor = None

    def setCursor(self, conn):
        self.cursor = conn.getCursor()

    def getCursor(self):
        return self.cursor

# getting all user records


class UsersGetting:
    userIds = []

    def __init__(self, cursor) -> None:
        self.cursor = cursor

    def getAllUsers(self):

        self.cursor.execute("select * from tbPerson")
        personData = self.cursor.fetchall()
        print(personData)
        return personData

    def getSpecificUser(self,userid):
        self.cursor.execute("select * from tbPerson where personId= ?",userid)
        
        imagespath = self.cursor.fetchall()
        for row in imagespath:
            print(row[1])
            return str(row[1])


    def gettingUserId(self):

        userdata = self.getAllUsers()
        for row in range(len(userdata)):

            self.userIds.append(userdata[row][0])
        return self.userIds

    def getUserAllLocations(self,userid):
        self.cursor.execute("select * from tbPersonLocation2 where personId= convert(int,?)",userid)
        rows=self.cursor.fetchall()
        return rows

    def getLocationNames(self):
        self.cursor.execute('Select locName from tbLocation')
        locationNames=[]
        output=self.cursor.fetchall()
        for x in output:
            locationNames.append(x[0])
        return locationNames


    def getSpecificDateTimespend(self, userid, date):
        self.cursor.execute(
            "select locId,SUM(timespend) as timeSpend from tbPersonLocation2 where personId=? and date=?  group by locId", userid, date)
        personTimespend = self.cursor.fetchall()
        return personTimespend


    def getUserLocationForPrediction(self,userid,date):
        self.cursor.execute(
            "select tbPersonLocation2.locId from tbPersonLocation2 where personId=? and date=format(CONVERT(date,?),'dd-MM-yy') order by substring(date,4,2) desc,substring(date,1,2) desc, time desc",userid,date
        )
        rows= self.cursor.fetchall()
        arr=[]
        for row in rows:
            print(row)    
            arr.append(row[0])
        return arr
        
    def getAllLocations(self):
        self.cursor.execute('Select locId,locName,latitude,longitude from tbLocation')
        locations=self.cursor.fetchall()
        return locations



    def getSpecificDateLocations(self, userid, date):
        self.cursor.execute(
            "select   * from tbPersonLocation2 where personId=convert(int,?) and date=? order by time desc", userid, date)
        personLocs = self.cursor.fetchall()
        return personLocs

    def getCurrentDateLocations(self, userid):
        self.cursor.execute(
            "select * from tbPersonLocation2 where personId=? and date=format(GETDATE(),'dd/MM/yy') order by time desc", userid)
        personLocs = self.cursor.fetchall()
        return personLocs

    def getAllLocationRecord(self, userid):
        self.cursor.execute(
            'Select * from tbPersonLocation2 where personId=?', userid)
        personLocs = self.cursor.fetchall()
        return personLocs

    def getUserLocations(self):

        self.cursor.execute('Select locId,personId from tbPersonLocation2')
        personLocs = self.cursor.fetchall()
        return personLocs

    def getUserLocationsById(self, userId):

        self.cursor.execute('select distinct locid,Max(time) from tbPersonLocation2 where personId=?',
                            userId, ' Group by locId order by Max(time) desc,locId')
        personLoc = self.cursor.fetchall()

        return personLoc


    # get last location id and last date time

    def getLastLocationId(self, userId):
        try:
            self.cursor.execute(
                'select top 1 locId,date,time from tbPersonLocation2 where personId= ? order by substring(date,4,2) desc,substring(date,1,2) desc,time desc', userId)
            rows = self.cursor.fetchall()
            for row in rows:

                return row.locId
        except Exception as e:
            print('Error: ', e)

    def getUserLastLocTime(self, userId):
        try:
            self.cursor.execute(
                'select top 1 date,time from tbPersonLocation2 where personId= ? order by substring(date,4,2) desc,substring(date,1,2) desc,time desc', userId)
            rows = self.cursor.fetchall()
            for row in rows:
                date = row.date
                time = row.time
                uDateTime = date+" "+time
                return uDateTime
        except Exception as e:
            print('Error: ', e)

    def getUserLocationNames(self, userId):
        userLocations = []
        try:
            self.cursor.execute('''select tbLocation.locName from tbLocation
                                    inner join tbPersonLocation
                                    on tbLocation.locId=tbPersonLocation.locId
                                    where tbPersonLocation.personId=?''', userId)
            rows = self.cursor.fetchall()
            for row in rows:
                userLocations.append(row.locName)
            return userLocations
        except Exception as e:
            print('error1:', e)

    def getUserLocationNameOrdered(self, userId):
        userLocations = []
        try:
            self.cursor.execute('select top 50 tbPersonLocation.locId,tbLocation.locName,SUBSTRING (time,0,6) from tbLocation inner join tbPersonLocation on tbLocation.locId=tbPersonLocation.locId where tbPersonLocation.personId=? order by substring(date,4,2) desc,substring(date,1,2) desc, time desc', userId)

            rows = self.cursor.fetchall()
            for row in rows:
                row[2] = row[2].split(':')
                row[2] = '.'.join(row[2])
                print(row)
                userLocations.append(row)

            return userLocations
        except Exception as e:
            try:
                print('error1:', e)
            finally:
                e = None
                del e

        # get lat long of areaLocation

    def getLatLong(self, locationId):

        self.cursor.execute(
            "select latitude,longitude from tbLocation where tbLocation.locId=?", locationId)
        data = self.cursor.fetchall()

        lat = data[0][0]
        long = data[0][1]
        long = float(long)

        lat = float(lat)

        return lat, long


# insert new user in database

class UserInsertion:
    def __init__(self, cursor) -> None:
        self.cursor = cursor

    def insertUser(self, user_id):
        try:

            self.cursor.execute('''
                        INSERT INTO tbPerson (personId, pName, imagesPath)
                        VALUES
                        (?,?,?)
                        
                        ''', user_id, 'user_'+str(user_id), 'images/user_'+str(user_id))
            self.cursor.commit()

            print('Saved to database')
        except:
            print('Already saved for this user')

    def insertUserLoc(self, user_id, locId, lat, long):

        now = datetime.now()

        currentTime = now.strftime("%H:%M")
        currentDate = now.strftime("%d/%m/%y")
        print(currentDate)

        self.cursor.execute('''
                insert into tbPersonLocation2(locId,personId,date,time,latitude,longitude,timespend)
                Values
                (?,?,?,?,?,?,?)
        ''', (locId, user_id, currentDate, currentTime, lat, long,1))

        self.cursor.commit()
        # cursor.close()


    def insertLocation(self,locname,latitude,longitude):
        self.cursor.execute('''
                insert into tbLocation(locName,latitude,longitude)
                Values
                (?,?,?)
        ''', (locname,latitude,longitude))
        self.cursor.commit()
        print('Location Saved to database')


    



