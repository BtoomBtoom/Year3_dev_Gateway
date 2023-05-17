from mqtt import Client
from dao import SqliteDAO
from logs import Log
import json
import os

def configDatabase(dbName, tableName):
    """Create database"""
    db = SqliteDAO(dbName)
    db.createTable(tableName, """id INTEGER NOT NULL, red INTEGER NOT NULL, green INTEGER NOT NULL, blue INTEGER NOT NULL, clear INTEGER NOT NULL,
                    light REAL NOT NULL, co2 INTEGER NOT NULL, dust REAL NOT NULL, tvoc REAL NOT NULL, motion INTEGER NOT NULL, sound REAL NOT NULL, 
                    temperature REAL NOT NULL, humidity REAL NOT NULL, time INTEGER NOT NULL, status INTEGER NOT NULL""")
    # db.listAllTables()
    # db.listAllColumns(tableName)

    return db

def configMQTT(broker, topic, port, db, tableName, logger):
    """MQTT connection"""
    client = Client()
    client.connect(broker, int(port), 60)

    while True:
        client.loop_start()
        client.subscribe(topic)
        while True:
            temp = client.msg_arrive()
            if temp != None:
                try: 
                    msg = json.loads(temp)
                    print(f"RECEIVE MESSAGE FROM BROKER {msg}")
                    # huimidity: correct letter humidity
                    db.insertOneRecord(tableName, f"""{msg['infor']['id']}, {msg['infor']['red']}, {msg['infor']['green']}, {msg['infor']['blue']}, 
                                        {msg['infor']['clear']}, {msg['infor']['light']}, {msg['infor']['co2']}, {msg['infor']['dust']}, 
                                        {msg['infor']['tvoc']}, {msg['infor']['motion']}, {msg['infor']['sound']}, {msg['infor']['temperature']}, 
                                        {msg['infor']['humidity']}, {msg['infor']['time']}, {msg['infor']['status']}""")
                except json.JSONDecodeError as error:
                    logger.exception(error)
                    print(str(error))
        client.loop_stop()

def main():
    print("Gateway start")

    logger = Log(__name__)
    try:
        logger.info("-------------Restart----------------")

        # câu lệnh os.environ.get(param1, param2) để lấy giá trị của key param1 
        # này ra trong đó param1 là environment variable còn 
        # param2 là để nếu như không tìm thấy environment variable này 
        # thì sẽ mặc định trả vế string param2
        #________________________________origin code_________________________
        # dbName = os.environ.get("DB_NAME", "data.db")
        #____________________________________________________________________
        dbName = "data.db"
        #____________________________________________________________________

        #________________________________origin code_________________________
        # tableName = os.environ.get("TABLE_NAME" ,"building")
        #____________________________________________________________________
        tableName = "farm"
        #____________________________________________________________________
        db = configDatabase(dbName, tableName)
        
        # broker = os.environ.get("MQTT_BROKER", "broker.mqttdashboard.com")
        broker = os.environ.get("MQTT_BROKER", "localhost") #desktop-rjl9d4n
        topic = os.environ.get("MQTT_TOPIC", "Year3/Gateway")
        port = os.environ.get("MQTT_PORT", 1883)
        configMQTT(broker, topic, port, db, tableName, logger)
    except KeyboardInterrupt as error:
        logger.error("Interrupt from keyboard")
        print(str(error))
    except Exception as error:
        print("_______________________________________________________")
        logger.exception(error)
        print(str(error))
    finally:
        logger.info("-------------End----------------")
    
    print("Gateway end")

if __name__ == "__main__":
    main()