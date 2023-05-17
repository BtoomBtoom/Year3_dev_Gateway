import sqlite3
# import puchikarui
from logs import Log    #class Log from logs.py
 
class SqliteDAO:
    """SQLite3 Data Access Object provides API to work with SQLite3 Database"""
    def __init__(self, dbLocation=None):
        if dbLocation is not None:
            self.__dbLocation = dbLocation
        else:
            self.__dbLocation = "data.db"  
        self.__logger = Log(__name__)
        # self.__logger.debug(self.__dbLocation)  
        # self.__logger.debug(type(self.__dbLocation))

    def __connect__(self):
        try: 
            self.__conn = sqlite3.connect(self.__dbLocation)
            self.__cursor = self.__conn.cursor()
        except sqlite3.Error as error:
            self.__logger.exception(error)
            
    # TODO: use *args, **kwargs
    # brief: method to execute a command
    #
    #
    def __do__(self, params):
        """
            params:
        """
        self.__cursor.execute(params)       # self.__cursor = self.__conn.cursor()  
        self.__conn.commit()                # self.__conn = sqlite3.connect(self.__dbLocation)

    # brief: method to close a connection to sqlite3
    # 
    #
    def __close__(self):
        self.__conn.close()

    # TODO: change print to log file
    # brief: method to create a table in sqlite3
    #       1. open a connection to a database
    #       2. execute the command "Create a table" in that database
    #       3. log the message to logger
    #       4. close the connection afterward
    def createTable(self, tableName, col):
        #__connect__()
        #__do__(): create
        #logger.infor()
        #logger.exception()
        #__close__()
        """Create a Table"""
        try:
            self.__connect__()
            table_check_command = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tableName}'"
            self.__cursor.execute(table_check_command)
            result = self.__cursor.fetchone()
            if result is None:
                print(f"{tableName} does not exist in the database")
                print(f"Start creating table {tableName}")
                self.__do__(f"CREATE TABLE {tableName} ({col});")
                self.__logger.info("Created table successfully")    #self.__logger = Log(__name__)
            else:
                print(f"{tableName} already exists in the database.")
        except sqlite3.Error as error:
            self.__logger.info("Created table unsuccessfully")
            self.__logger.exception(error)
        finally:
            self.__close__()
    
    # brief: method to insert a record to a tableName
    #       1. open a connection to a database
    #       2. execute the command "Insert data to table" in that database
    #       3. log the message to logger
    #       4. close the connection afterward
    def insertOneRecord(self, tableName, colValues):
        try:
            self.__connect__()
            self.__do__(f"INSERT INTO {tableName} VALUES ({colValues});")
            print("Successfully insert to database!")
            self.__logger.info("Inserted a record successfully")
        except sqlite3.Error as error:
            self.__logger.info("Insertted a record unsuccessfully")
            self.__logger.exception(error)            
        finally:
            self.__close__()

    # brief: method to retrieve all tables that are currently available in database
    #       1. open a connection to a database
    #       2. execute the command "SELECT name FROM sqlite_master WHERE type='table';" in that database
    #       3. log the message to logger
    #       4. close the connection afterward
    def listAllTables(self):
        """Show all tables in database"""
        self.__connect__()
        self.__do__("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.__cursor.fetchall()
        print(tables) if len(tables) != 0 else print(None)
        self.__close__()
 

    def listAllColumns(self, tableName):
        self.__connect__()
        self.__cursor.execute(f"SELECT sql FROM sqlite_master WHERE tbl_name = '{tableName}' AND type = 'table';")
        # self.__cursor.execute("PRAGMA table_info('{}');".format(tableName))
        colNames = self.__cursor.fetchall()
        print(colNames) if len(colNames) != 0 else print(None) 
        self.__close__()

    def listAllValues(self, tableName):
        try:
            self.__connect__()
            self.__do__(f"SELECT * FROM {tableName};")
            res = self.__cursor.fetchall()
            #self.__logger.debug(res)
            self.__logger.info("Retrieved all values successfully")
        except sqlite3.Error as error:
            self.__logger.info("Retrieved all values unsuccessfully")
            self.__logger.exception(error)
        finally:
            self.__close__()
    
    # DISCLAIMED: These functions have not been tested
    # UPDATE
    # TODO: use rowid
    def updateOneRecord(self, tableName, new, condition):
        try:
            self.__connect__()
            self.__do__(f"UPDATE {tableName} SET {new} WHERE {condition}")
            self.__logger.info("Updated a record successfully")
        except sqlite3.Error as error:
            self.__logger.info("Updated a record unsuccessfully")
            self.__logger.exception(error)
        finally:
            self.__close__()
    
    # DELETE
    def deleteOneRecord(self, tableName, condition):
        try:
            self.__connect__()
            self.__do__(f"DELETE FROM {tableName} WHERE {condition}")
            self.__logger.info("Deleted a record successfully")
        except sqlite3.Error as error:
            self.__logger.info("Deleted a record unsuccessfully")
            self.__logger.exception(error)
        finally:
            self.__close__()     

if __name__=="__main__":
    pass        