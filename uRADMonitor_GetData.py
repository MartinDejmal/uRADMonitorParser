import sys
import time
import datetime
from time import sleep, strftime
from datetime import datetime
import mysql.connector
from mysql.connector import errorcode
import urllib.request, json 

config = {
  'user': 'iot',
  'password': 'myStrongPassword',
  'host': '192.168.0.250',
  'database': 'iot',
  'raise_on_warnings': True,
}

debug = 0 

try:
  if debug: print(datetime.now().strftime('%d.%m. %H:%M') + " (I) Connecting to database.")
  cnx = mysql.connector.connect(**config)
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print(datetime.now().strftime('%d.%m. %H:%M') + " (E) SQL Access Denied error.")
  else:
    print(datetime.now().strftime('%d.%m. %H:%M') + " (E) SQL Error: "  + err)
reconnectdb = 0 
sqlins="insert into iot.Reading (Value, rSensorId) values (%s, %s);"
sqlupd="update iot.Sensor set LastUpdate=now(), ValueLast=%s where idSensor=%s;"
cursor = cnx.cursor()
isvalid = 1

with urllib.request.urlopen("http://192.168.0.168/j") as url:
  data = json.loads(url.read().decode())
  data = data['data']
if debug:
  print(datetime.now().strftime('%d.%m. %H:%M') + " (I) Returned data:")
  print('  Station ID: ', data['id'])
  print('  Radiation:  ', round(data['cpm']*0.0066,2))
  print('  Temp:       ', data['temperature'], 'C')
  print('  Pressure:   ', data['pressure'], 'Pa')
  print('  Humidity:   ', data['humidity'], '% RH')
if (data['id'] != "13DAFF54" ):
  print(datetime.now().strftime('%d.%m. %H:%M') + " (W) This station is unknown.")
  isvalid = 1
elif (data['humidity'] > 100):
  print(datetime.now().strftime('%d.%m. %H:%M') + " (E) Invalid humidity reading.")
  isvalid = 0
if isvalid:
  try:
    if debug: print(datetime.now().strftime('%d.%m. %H:%M') + " (I) Saving dataword to DB.")
    if reconnectdb:
      print(datetime.now().strftime('%d.%m. %H:%M') + " (I) Reconnecting to the database.")
      cnx.reconnect()
      reconnectdb=0

    sensordata = (round(data['cpm']*0.0066,2), 30)
    cursor.execute(sqlins,sensordata)
    cursor.execute(sqlupd,sensordata)

    sensordata = (data['temperature'], 31)
    cursor.execute(sqlins,sensordata)
    cursor.execute(sqlupd,sensordata)

    sensordata = (data['humidity'], 32)
    cursor.execute(sqlins,sensordata)
    cursor.execute(sqlupd,sensordata)

    sensordata = (round(data['pressure']/100,2), 33)
    cursor.execute(sqlins,sensordata)
    cursor.execute(sqlupd,sensordata)

    cnx.commit()
  except mysql.connector.Error as err:
    print(datetime.now().strftime('%d.%m. %H:%M') + " (E) Unsuccessful DB commit: "+ str(err))
    reconnectdb=1
    isvalid = 1
else:
  print(datetime.now().strftime('%d.%m. %H:%M') + " (W) Data word invalid, not saving to DB.")
  isvalid = 1
sys.stdout.flush()
cnx.close()
cursor.close()
if debug: print(datetime.now().strftime('%d.%m. %H:%M') + " (I) Normal exit.")
