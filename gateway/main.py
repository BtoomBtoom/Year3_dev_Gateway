from mqtt import Client
from dao import SqliteDAO
from logs import Log
import json
import os
import multiprocessing
import threading
import time
import sqlite3
import time as clock
import calendar
import datetime
import subprocess

def configDatabase(dbName) -> None:
    """Create database"""
    # Enable foreign key constraints
    print("Turned on foreign_keys constrain")
    db = SqliteDAO(dbName)
    table_name_Registration = "Registration"
    table_name_SensorMonitor = "SensorMonitor"
    table_name_ActuatorMonitor = "ActuatorMonitor"
    table_name_SetPointControl = "SetPointControl"
    create_table_Registration: str = """id INTEGER PRIMARY KEY, 
                                        macAddress TEXT(20)"""
    create_table_SensorMonitor: str = """id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        node_id INTEGER,
                                        co2 INTEGER,
                                        temp REAL,
                                        hum REAL,
                                        time INTEGER,
                                        FOREIGN KEY (node_id) REFERENCES Registration(node_id) ON DELETE CASCADE ON UPDATE CASCADE"""
    create_table_ActuatorMonitor: str = """id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        node_id INTEGER,
                                        speed INTEGER,
                                        state INTEGER,
                                        time INTEGER,
                                        FOREIGN KEY (node_id) REFERENCES Registration(node_id) ON DELETE CASCADE ON UPDATE CASCADE"""
    create_table_SetPointControl: str = """id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        node_id INTEGER,
                                        aim TEXT(10),
                                        value REAL,
                                        time INTEGER,
                                        FOREIGN KEY (node_id) REFERENCES Registration(node_id) ON DELETE CASCADE ON UPDATE CASCADE"""
    \
    db.createTable(table_name_Registration, create_table_Registration)
    db.createTable(table_name_SensorMonitor, create_table_SensorMonitor)
    db.createTable(table_name_ActuatorMonitor, create_table_ActuatorMonitor)
    db.createTable(table_name_SetPointControl, create_table_SetPointControl)

    # db.createTable(table_name_1, """node_id INTEGER NOT NULL, co2 INTEGER NOT NULL, temp REAL NOT NULL, hum REAL NOT NULL, time INTEGER NOT NULL""")
    # db.createTable(table_name_2, """node_id INTEGER NOT NULL, state INTEGER NOT NULL, speed INTEGER NOT NULL, time INTEGER NOT NULL""")
    # db.listAllTables()
    # db.listAllColumns(tableName)

def registerNode(dbName) -> None:
    pass

def configMQTT(broker, topic, port, dbName,lock):
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
                    msg = json.loads(temp)  #decode json-file to normal dictionary
                    print(f"receive message from broker {broker}: {msg}")
                    # huimidity: correct letter humidity
                    with lock:
                        db = SqliteDAO(dbName)
                        logger = Log(__name__)
                        print("START INSERTING DATA TO DATABASE")
                        if topic == "farm/1/sensor/1":
                            colValuesTuple = []
                            colValuesTuple.append(1)
                            for key in msg:
                                if key == "info":
                                    for info_key in msg[key]:
                                        colValuesTuple.append(msg[key][info_key])
                            colValuesTuple = tuple(colValuesTuple)
                            print(colValuesTuple)
                            db.insertOneRecord("SensorMonitor",
                                               "node_id, co2, temp, hum, time",
                                                "?, ?, ?, ?, ?", colValuesTuple)
                        elif topic == "farm/1/actuator/1":
                            colValuesTuple = []
                            colValuesTuple.append(1)
                            for key in msg:
                                if key == "info":
                                    for info_key in msg[key]:
                                        colValuesTuple.append(msg[key][info_key])
                            colValuesTuple = tuple(colValuesTuple)
                            print(colValuesTuple)
                            db.insertOneRecord("ActuatorMonitor",
                                               "node_id, state, speed, time", 
                                                "?, ?, ?, ?", colValuesTuple)
                            #INSERT INTO ActuatorMonitor VALUES (1, 0, 63, 1684639109);
                except json.JSONDecodeError as error:
                    
                    logger.exception(error)
                    print(str(error))
        client.loop_stop()

"""
* brief: This function is to get the lastest 10 data from the database and then
    compute out the average value of those and send that back to backend with 
    current time, of course this will be handled with it's own process, and this function will 
    run every 5 seconds for simpicity
"""
def sendSensorToBackend(broker, topic1,topic2, port, dbName, sensorTableName, actuatorTableName, 
                        number_of_latest_data, time_delay, lock):
    #create a client and connect that to broker
    client = Client()
    client.connect(broker, int(port), 60)
    while(True):  
        client.loop_start()
        client.subscribe(topic1)
        client.subscribe(topic2)
        while(True):
            with lock:
                date = datetime.datetime.utcnow()
                utc_time = calendar.timegm(date.utctimetuple())
                [co2, temp, hum] = getAverageData(dbName, sensorTableName, number_of_latest_data, datatype="sensor")
                [speed, state, time] = getAverageData(dbName, actuatorTableName, datatype="actuator")
                if co2 != None and state != None:
                    new_sensor_data = { 
                                        "operator": "dataResponse", 
                                        "status": 0, 
                                        "info": { 
                                            "co2": co2, 
                                            "temp": temp, 
                                            "hum": hum, 
                                            "time": utc_time,
                                        } 
                                    } 

                    new_actuator_data = { 
                            "operator": "actuatorData", 
                            "status": 0, 
                            "info": 
                            { 
                                "state": state, 
                                "speed": speed, 
                                "time": time,
                            } 
                        }
                    client.publish(topic1, json.dumps(new_sensor_data))
                    print("successfully publish SENSORDATA to DJANGO ") #+ str(new_sensor_data))
                    client.publish(topic2, json.dumps(new_actuator_data))
                    print("successfully publish ACTUATORDATA to DJANGO") #+ str(new_actuator_data))
                    clock.sleep(time_delay)            
                else:
                    print("No data to publish to back-end")
                    clock.sleep(time_delay)    
    client.loopstop()


"""
*brief: this function is to get the needed number of latest data in database and
        compute out the average value of those
*return: a list of [co2, temp, hum]
"""
def getAverageData(dbName, tableName, number_of_latest_data=10, datatype="sensor") -> list:
    __conn = sqlite3.connect(dbName)
    __cur = __conn.cursor()
    if datatype == "sensor":
        res = __cur.execute(f"SELECT * FROM {tableName} ORDER by time DESC LIMIT {number_of_latest_data};")
        res_list = res.fetchall()
        __cur.close()
        __conn.close()
        res_data = {"co2": 0, "temp": 0, "hum": 0}
        if len(res_list) != 0:
            for i in res_list:
                res_data["co2"] += i[2]
                res_data["temp"] += i[3]
                res_data["hum"] += i[4]
            return [round(res_data["co2"]/number_of_latest_data), round(res_data["temp"]/number_of_latest_data), round(res_data["hum"]/number_of_latest_data)]
        else:
            print("No data")
            return [None, None, None]    
    elif datatype == "actuator":
        res = __cur.execute(f"SELECT * FROM {tableName} ORDER by time DESC LIMIT 1;")
        res_list = res.fetchall()
        __cur.close()
        __conn.close()
        if len(res_list) != 0:
            # print("RES LIST ACTUATORRRRRRRRRRRRRRRRRRRRRRR")
            # print(res_list)
            res_data = {"speed": res_list[0][2], "state": res_list[0][3], "time": res_list[0][4]}
            # print("RES DATA ACTUATORRRRRRRRRRRRRRRRRRRRRRRRRRRR")
            # print(res_data)
            return [res_data["speed"],res_data["state"], res_data["time"]]
        else:
            print("No data")
            return [None, None, None]

def main():
    cmd_command: str = "emqx start"
    subprocess.run(cmd_command, shell = True)
    print("EMQX start")
    print("Gateway start")
    #add some fake nodes with their macaddress into table

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
        # tableName = "farm"
        #____________________________________________________________________
        configDatabase(dbName)
        #add some fake registered nodes into database
        # registerNode(dbName)
        
        # broker = os.environ.get("MQTT_BROKER", "broker.mqttdashboard.com")
        broker = os.environ.get("MQTT_BROKER", "localhost") #desktop-rjl9d4n
        # topic = os.environ.get("MQTT_TOPIC", "Year3/Gateway")
        topic_list = {"sensor_topic": "farm/1/sensor/1", 
                      "actuator_topic": "farm/1/actuator/1",
                      "sensor_gateway_server": "farm/1/monitor",
                      "actuator_gateway_server": "farm/1/monitor/process",}
        port = os.environ.get("MQTT_PORT", 1883)
        lock = multiprocessing.Lock()
        process_list = []
        process_list.append(multiprocessing.Process(target=configMQTT, args=(broker, topic_list["sensor_topic"], port, dbName, lock)))
        process_list.append(multiprocessing.Process(target=configMQTT, args=(broker, topic_list["actuator_topic"], port, dbName, lock)))
        process_list.append(multiprocessing.Process(target=sendSensorToBackend, args=(
                                                            broker, topic_list["sensor_gateway_server"], 
                                                            topic_list["actuator_gateway_server"], 
                                                            port, dbName, "SensorMonitor", 
                                                            "ActuatorMonitor",
                                                            10, 8, lock
                                                        )))
        for i in process_list:
            i.start()   
        for i in process_list:
            i.join()
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
    cmd_command = "emqx stop"
    subprocess.run(cmd_command, shell = True)
    print("EMQX stop")

if __name__ == "__main__":
    main()