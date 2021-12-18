
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
    
    def getAllUsers(self,cursor):
        cursor=cursor
        cursor.execute("Select * from tbPerson")
        personData=cursor.fetchall()
        print(personData)
        return personData


# getting all user ids
class UserIdsGetting:
    
    userIds=[]

    def gettingUserId(self,cursor):

        users=UsersGetting()    
        userdata=users.getAllUsers(cursor)
        for row in range(len(userdata)):
            # personIds.append(row[0])
            # personNames.append(row[1])
            self.userIds.append( userdata[row][0])
        return self.userIds

    def getUserLocations(self,cursor):
        cursor=cursor
        cursor.execute('Select locId,personId from tbPersonLocation')
        personLocs=cursor.fetchall()
        return personLocs
# insert new user in database

class UserInsertion:
    # run=0
    # currentTime=0
    # startTime = time.time()
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
    
    def insertUserLoc(self,cursor,user_ids,locId,userlocs):
        cursor=cursor
        # if(UserInsertion.run==0):
            # currentTime=datetime.datetime.now()
        
        now = datetime.now()
        print('Now =: ',now)
        currentTime=now.strftime("%H:%M:%S")

        # try:
        # print(currentTime)
        # time.sleep(3.0 - ((time.time() - UserInsertion.startTime) % 3.0))
        for userid in user_ids:
            # if(not userid==userlocs):
            cursor.execute('''
                    insert into tbPersonLocation(locId,personId,time)
                    Values
                    (?,?,?)
            ''',(locId,userid,currentTime))
            cursor.commit()
            # cursor.close()
            print('location added!')

                # else:
                #     print('The person is already at that location')
        # except Exception:
        #     print(str(Exception))

        # def timeupdate(currenttime):



       # for i in range(len(userlocs)):
        #     if(user_id userlocs[i][1]):
        #         cursor.execute('''
        #                 insert into tbPersonLocation(locId,personId,time)
        #                 Values
        #                 (?,?,?)
        #         ''',(locId,user_id,str(self.currentTime)))
        #         cursor.commit()
        #         cursor.close()
        #         print('location added!')
        #     else:
        #         print('The person is already at that location')
                
        # for i in range(len(userlocs)):
        #     if(not user_ids[i]==userlocs[i][1]):
        #         cursor.execute('''
        #                 insert into tbPersonLocation(locId,personId,time)
        #                 Values
        #                 (?,?,?)
        #         ''',(locId,user_ids[i],str(self.currentTime)))
        #         cursor.commit()
        #         cursor.close()
        #         print('location added!')
        #  