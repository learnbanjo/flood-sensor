from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID,DEVICE_LOCATION
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
P="1.0"
f=5
G="spBv1.0/flood_sensors"
j="spBv1.0/flood_sensors/DCMD"
S="spBv1.0/flood_sensors/DDATA/"+DEVICE_LOCATION+"/"+DEVICE_NAME
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 R=ADC(ANALOG_SENSOR_PIN)
else:
 R=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 g=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 g=""
s=mqtt_broker_address
u=ubinascii.hexlify(DEVICE_NAME)
V=b'spBv1.0/flood_sensors/DCMD'
W=b'spBv1.0/flood_sensors/DDATA/'+DEVICE_LOCATION+'/'+DEVICE_NAME
print(W)
E=0
w=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'spBv1.0/flood_sensors/DCMD':
  print('ESP received DCMD message')
  t="\"name\":\"OTA\""
  p="\"name\":\"status\""
  A="\"deviceName\":\""+DEVICE_NAME+"\""
  Q="\"deviceName\":\"*\"" 
  b=msg.decode()
  if t in b and(A in b or Q in b):
   print('ESP received CMD message: OTA')
   N=json.loads(b)
   from ota import OTAUpdater
   l="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   i=N.get("otafiles")
   n=True
   b=DEVICE_NAME+" OTA: "+i
   try:
    C=OTAUpdater(l,i)
    if C.check_for_updates():
     if C.download_and_install_update():
      b+=" updated"
     else:
      b+=" update failed"
    else:
     b+=" up-to-date" 
     n=False
   except Exception as F:
    b+=" err:"+str(F)+" type:"+str(type(F))
   finally:
    print(b)
    r.publish(S,b)
    time.sleep(5)
    if n:
     machine.reset() 
  elif p in b:
   print('ESP received CMD message: status')
   r.publish(W,create_sensor_message())
def connect_and_subscribe():
 global u,s,V
 r=MQTTClient(u,s)
 r.set_callback(sub_cb)
 r.connect()
 r.subscribe(V)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(s,V))
 return r
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global R
 global g
 b="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(R!=""):
  b=b+",\"AnaR\":\""+str(R.read())+"\""
 if(g!=""):
  b=b+",\"DigR\":\""+str(g.value())+"\""
 if error!="":
  b=b+",\"err\":\""+error+"\""
 return b+"}"
try:
 r=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  r.check_msg()
  if(time.time()-E)>w:
   r.publish(W,create_sensor_message())
   E=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

