from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID,DEVICE_LOCATION
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
f="1.0"
r=5
n="pBv1.0/flood_sensors"
E="pBv1.0/flood_sensors/DCMD"
h="pBv1.0/flood_sensors/DDATA/"+DEVICE_LOCATION+"/"+DEVICE_NAME
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 I=ADC(ANALOG_SENSOR_PIN)
else:
 I=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 s=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 s=""
c=mqtt_broker_address
p=ubinascii.hexlify(DEVICE_NAME)
X=b'pBv1.0/flood_sensors/DCMD'
D=b'pBv1.0/flood_sensors/DDATA/'+DEVICE_LOCATION+'/'+DEVICE_NAME
print(D)
Y=0
x=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'pBv1.0/flood_sensors/DCMD':
  print('ESP received DCMD message')
  C="\"name\":\"OTA\""
  w="\"name\":\"status\""
  d="\"deviceName\":\""+DEVICE_NAME+"\""
  l="\"deviceName\":\"*\"" 
  R=msg.decode()
  if C in R and(d in R or l in R):
   print('ESP received CMD message: OTA')
   P=json.loads(R)
   from ota import OTAUpdater
   T="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   v=P.get("otafiles")
   U=True
   R=DEVICE_NAME+" OTA: "+v
   try:
    W=OTAUpdater(T,v)
    if W.check_for_updates():
     if W.download_and_install_update():
      R+=" updated"
     else:
      R+=" update failed"
    else:
     R+=" up-to-date" 
     U=False
   except Exception as O:
    R+=" err:"+str(O)+" type:"+str(type(O))
   finally:
    print(R)
    K.publish(h,R)
    time.sleep(5)
    if U:
     machine.reset() 
  elif w in R:
   print('ESP received CMD message: status')
   K.publish(D,create_sensor_message())
def connect_and_subscribe():
 global p,c,X
 K=MQTTClient(p,c)
 K.set_callback(sub_cb)
 K.connect()
 K.subscribe(X)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(c,X))
 return K
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global I
 global s
 R="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(I!=""):
  R=R+",\"AnaR\":\""+str(I.read())+"\""
 if(s!=""):
  R=R+",\"DigR\":\""+str(s.value())+"\""
 if error!="":
  R=R+",\"err\":\""+error+"\""
 return R+"}"
try:
 K=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  K.check_msg()
  if(time.time()-Y)>x:
   K.publish(D,create_sensor_message())
   Y=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

