# import sqlite3

# __conn = sqlite3.connect("data.db")
# __cur = __conn.cursor()
# res = __cur.execute("INSERT INTO SensorMonitor (node_id, co2, temp, hum, time) VALUES (?, ?, ?, ?, ?)", 
#                     (1, 1975, 61.84, 67.85, 1684650241))
# res = __cur.execute("INSERT INTO SensorMonitor (node_id, co2, temp, hum, time) VALUES (?, ?, ?, ?, ?)", 
#                     (1, 1975, 61.84, 67.85, 1684650241))
# res = __cur.execute("INSERT INTO SensorMonitor (node_id, co2, temp, hum, time) VALUES (?, ?, ?, ?, ?)", 
#                     (1, 1975, 61.84, 67.85, 1684650241))
# res = __cur.execute("INSERT INTO SensorMonitor (node_id, co2, temp, hum, time) VALUES (?, ?, ?, ?, ?)", 
#                     (1, 1975, 61.84, 67.85, 1684650241))
# res = __cur.execute("INSERT INTO SensorMonitor (node_id, co2, temp, hum, time) VALUES (?, ?, ?, ?, ?)", 
#                     (1, 1975, 61.84, 67.85, 1684650241))
# res = __cur.execute("INSERT INTO SensorMonitor (node_id, co2, temp, hum, time) VALUES (?, ?, ?, ?, ?)", 
#                     (1, 1975, 61.84, 67.85, 1684650241))
# res = __cur.execute("INSERT INTO SensorMonitor (node_id, co2, temp, hum, time) VALUES (?, ?, ?, ?, ?)", 
#                     (1, 1975, 61.84, 67.85, 1684650241))
# res = __cur.execute("INSERT INTO SensorMonitor (node_id, co2, temp, hum, time) VALUES (?, ?, ?, ?, ?)", 
#                     (1, 1975, 61.84, 67.85, 1684650241))
# print(type((1, 1975, 61.84, 67.85, 1684650241)))
# __conn.commit()

# res = __cur.execute("SELECT * FROM SensorMonitor ORDER by time DESC LIMIT 5")
# res_list = res.fetchall()
# __cur.close()
# __conn.close()
# print(res_list)


# # import subprocess

# # cmd_command: str = "emqx start"
# # subprocess.run(cmd_command, shell = True)


# class Test:
#     def func(self, arg1, arg2 = "hello"):
#         print("Hey" + str(arg2))
#     def override_func(self):
#         print(self.__class__ )
# def func(arg1, agr2 = "????") -> None:
#     print("This is function func" + str(agr2))

# t1 = Test()
# def override_func(msg):
#     print("This is override function with data "+str(msg))
# t1.override_func = override_func
# t1.func(arg1 = "lol", arg2 = "hehe")
# t1.override_func("TEST DATA")

# func(arg1="func test")

broker = "27.71.227.1"
import mqtt as mqtt_client
client = mqtt_client.Client()
client.connect(broker, int(1883), 60)
client.subscribe("farm/1/control")
client.subscribe("farm/1/monitor")
client.subscribe("farm/1/monitor/process")

client.loop_start()
def on_message(client, userdata, mes):
    msg = mes.payload.decode("utf-8")
    print(msg)
client.on_message = on_message
while(1):
    pass

# import multiprocessing
# print(f"There are currently {multiprocessing.active_children} process running")