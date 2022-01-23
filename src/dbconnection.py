import pyodbc

# database connection class
class DbConnection:
    def __init__(self) -> None:
        self.cursor=None
    def getCursor(self):
        return self.cursor
    def connectToDb(self):

        # creating connection
        connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=TAQILAPTOP\SQLEXPRESS2019;DATABASE=TaqiComputers_DB;Trusted_Connection=yes;')
        connection.autocommit=True
        self.cursor=connection.cursor()
        print("Connection successful")
        
    