from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import MQTT_BROKER_ADD,MQTT_BROKER_PORT,MQTT_KEEP_ALIVE_TIME,MQTT_PUBLISH_INTERVAL
from DEVICE_CONFIG import SPARKPLUGB_GID,SPARKPLUGB_EONID
from HW_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from utils import get_epoch_time
import json
import machine
import time
import ubinascii
from umqtt.simple import MQTTClient
A="1.0"
n="spBv1.0/"+SPARKPLUGB_GID
H=n+"/DCMD"
P=n+"/DDATA/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
e=n+"/DBIRTH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
X=n+"/DDEATH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
q=5
R=DEVICE_NAME.encode()
v=", \"device_id\": \""+DEVICE_NAME+"\""
c=H.encode()
g=P.encode()
u=0
def reboot_with_reason(V,reason=0):
 h=get_sparkplug_prefx()+",\"ddeath_reasons\": \""+str(reason)+"\"}"
 V.publish(X.encode(),h.encode)
 V.disconnect()
 time.sleep(5)
 machine.reset() 
def get_sparkplug_prefx():
 global u
 if u>=2147483647:
  u=0
 u+=1
 return "{\"timestamp: \""+str(get_epoch_time())+v+",\"seq\": \""+str(u)+"\""
def sub_cb(topic,msg):
 if topic==c:
  I="\"device_id\":\""+DEVICE_NAME+"\""
  h=msg.decode()
  if(I in h or "\"device_id\":\"*\"" in h):
   if "\"cmdID\":\"OTA\"" in h:
    k=json.loads(h)
    from ota import OTAUpdater
    C="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
    o=k['payload'][0]['otafiles']
    W=True
    h=DEVICE_NAME+" OTA: "+o
    try:
     Q=OTAUpdater(C,o)
     if Q.check_for_updates():
      if Q.download_and_install_update():
       h+=" updated"
      else:
       h+=" update failed"
     else:
      h+=" up-to-date" 
      W=False
    except Exception as y:
     h+=" err:"+str(y)+" type:"+str(type(y))
    finally:
     print(h)
     V.publish(P,h)
     if W:
      reboot_with_reason(V,DDEATH_REASON_OTA)
   elif "\"cmdID\":\"status\"" in h:
    V.publish(g,create_sensor_message())
   elif "\"cmdID\":\"reset\"" in h:
    reboot_with_reason(V,DDEATH_REASON_DCMD_REBOOT)
def connect_and_subscribe():
 global R,c
 V=MQTTClient(R,MQTT_BROKER_ADD)
 V.set_callback(sub_cb)
 h=get_sparkplug_prefx()+",\"ddeath_reasons\": \"-1\"}"
 V.set_last_will(X,h.encode())
 V.connect()
 V.subscribe(c)
 G=get_sparkplug_prefx()+"}"
 V.publish(e.encode(),G.encode())
 return V
def restart_and_reconnect():
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global E
 global i
 h=get_sparkplug_prefx()+",\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(E!=""):
  h=h+",\"AnaR\":\""+str(E.read())+"\""
 if(i!=""):
  h=h+",\"DigR\":\""+str(i.value())+"\""
 if error!="":
  h=h+",\"err\":\""+error+"\""
 return h+"}"
E=""
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 E=ADC(ANALOG_SENSOR_PIN)
i=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 i=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
try:
 V=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
j=0
while True:
 try:
  V.check_msg()
  if(time.time()-j)>MQTT_PUBLISH_INTERVAL:
   V.publish(g,create_sensor_message().encode())
   j=time.time()
 except Exception as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

