import sqlite3

__conn = sqlite3.connect("data.db")
__cur = __conn.cursor()
res = __cur.execute("INSERT INTO SensorMonitor (node_id, co2, temp, hum, time) VALUES (?, ?, ?, ?, ?)", 
                    (1, 1975, 61.84, 67.85, 1684650241))
res = __cur.execute("INSERT INTO SensorMonitor (node_id, co2, temp, hum, time) VALUES (?, ?, ?, ?, ?)", 
                    (1, 1975, 61.84, 67.85, 1684650241))
res = __cur.execute("INSERT INTO SensorMonitor (node_id, co2, temp, hum, time) VALUES (?, ?, ?, ?, ?)", 
                    (1, 1975, 61.84, 67.85, 1684650241))
res = __cur.execute("INSERT INTO SensorMonitor (node_id, co2, temp, hum, time) VALUES (?, ?, ?, ?, ?)", 
                    (1, 1975, 61.84, 67.85, 1684650241))
res = __cur.execute("INSERT INTO SensorMonitor (node_id, co2, temp, hum, time) VALUES (?, ?, ?, ?, ?)", 
                    (1, 1975, 61.84, 67.85, 1684650241))
res = __cur.execute("INSERT INTO SensorMonitor (node_id, co2, temp, hum, time) VALUES (?, ?, ?, ?, ?)", 
                    (1, 1975, 61.84, 67.85, 1684650241))
res = __cur.execute("INSERT INTO SensorMonitor (node_id, co2, temp, hum, time) VALUES (?, ?, ?, ?, ?)", 
                    (1, 1975, 61.84, 67.85, 1684650241))
res = __cur.execute("INSERT INTO SensorMonitor (node_id, co2, temp, hum, time) VALUES (?, ?, ?, ?, ?)", 
                    (1, 1975, 61.84, 67.85, 1684650241))
print(type((1, 1975, 61.84, 67.85, 1684650241)))
__conn.commit()

res = __cur.execute("SELECT * FROM SensorMonitor ORDER by time DESC LIMIT 5")
res_list = res.fetchall()
__cur.close()
__conn.close()
print(res_list)


# import subprocess

# cmd_command: str = "emqx start"
# subprocess.run(cmd_command, shell = True)