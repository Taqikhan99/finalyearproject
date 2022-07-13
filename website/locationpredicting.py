import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
import pyodbc



def locationPrediction():

    connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-3P0102M\SQLEXPRESS;DATABASE=TaqiComputers_DB;Trusted_Connection=yes;')
    cursor=connection.cursor()
    print("Connected")
    query=cursor.execute('''select top 20 tbPersonLocation.locId as locid,SUBSTRING (time,0,6) as time,tbLocation.locName as lastLocation from tbPersonLocation
    inner join tbLocation on tbPersonLocation.locId=tbLocation.locId
    where tbPersonLocation.personId=4 order by  substring(date,4,2) desc,substring(date,1,2) desc, time desc''')
    rows = cursor.fetchall()
    for row in rows:
        row[1] = row[1].split(":")
        row[1] = ".".join(row[1])

    df = pd.DataFrame(np.reshape(rows,(df.shape[0],3)), columns = ['locid', 'time', 'lastLocation'])
    df['time'] = df['time'].astype(float)
    print(df['time'])

    a=pd.DataFrame(rows)
    print(a)

    # %matplotlib inline
    plt.xlabel('Time')
    plt.ylabel('location')
    plt.scatter(df.time,df.lastLocation,color='red',marker='+')
    plt.xlim(df['time'].min(),df['time'].max()+1)

    print(df.shape)
    from sklearn.model_selection import train_test_split  

    X_train,X_test,y_train,y_test=train_test_split(df[['time']],df.lastLocation,train_size=0.9)
    X_test

    X_train

    model=linear_model.LogisticRegression()
    model.fit(X=X_train,y=y_train)
    model.predict(X_test)

    model.score(X_test,y_test)

    model.predict_proba(X_test)