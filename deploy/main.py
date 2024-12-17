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
m="1.0"
q="spBv1.0/"+SPARKPLUGB_GID
j=q+"/DCMD"
L=q+"/DDATA/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
k=q+"/DBIRTH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
N=q+"/DDEATH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
f=5
M=DEVICE_NAME.encode()
h=", \"device_id\": \""+DEVICE_NAME+"\""
T=j.encode()
R=L.encode()
Q=0
def reboot_with_reason(w,reason=0):
 o=get_sparkplug_prefx()+",\"ddeath_reasons\": \""+str(reason)+"\"}"
 w.publish(N.encode(),o.encode)
 w.disconnect()
 time.sleep(5)
 machine.reset() 
def get_sparkplug_prefx():
 global Q
 if Q>=2147483647:
  Q=0
 Q+=1
 return "{\"timestamp: \""+str(get_epoch_time())+h+",\"seq\": \""+str(Q)+"\""
def sub_cb(topic,msg):
 if topic==T:
  I="\"device_id\":\""+DEVICE_NAME+"\""
  o=msg.decode()
  if(I in o or "\"device_id\":\"*\"" in o):
   if "\"cmdID\":\"OTA\"" in o:
    C=json.loads(o)
    from ota import OTAUpdater
    d="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
    U=C['payload'][0]['otafiles']
    u=True
    o=DEVICE_NAME+" OTA: "+U
    try:
     y=OTAUpdater(d,U)
     if y.check_for_updates():
      if y.download_and_install_update():
       o+=" updated"
      else:
       o+=" update failed"
     else:
      o+=" up-to-date" 
      u=False
    except Exception as s:
     o+=" err:"+str(s)+" type:"+str(type(s))
    finally:
     print(o)
     w.publish(L,o)
     if u:
      reboot_with_reason(w,DDEATH_REASON_OTA)
   elif "\"cmdID\":\"status\"" in o:
    w.publish(R,create_sensor_message())
   elif "\"cmdID\":\"reset\"" in o:
    reboot_with_reason(w,DDEATH_REASON_DCMD_REBOOT)
def connect_and_subscribe():
 global M,T
 w=MQTTClient(M,MQTT_BROKER_ADD)
 w.set_callback(sub_cb)
 o=get_sparkplug_prefx()+",\"ddeath_reasons\": \"-1\"}"
 w.set_last_will(N,o.encode())
 w.connect()
 w.subscribe(T)
 B=get_sparkplug_prefx()+"}"
 w.publish(k.encode(),B.encode())
 return w
def restart_and_reconnect():
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global W
 global v
 o=get_sparkplug_prefx()+",\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(W!=""):
  o=o+",\"AnaR\":\""+str(W.read())+"\""
 if(v!=""):
  o=o+",\"DigR\":\""+str(v.value())+"\""
 if error!="":
  o=o+",\"err\":\""+error+"\""
 return o+"}"
W=""
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 W=ADC(ANALOG_SENSOR_PIN)
v=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 v=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
try:
 w=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
H=0
while True:
 try:
  w.check_msg()
  if(time.time()-H)>MQTT_PUBLISH_INTERVAL:
   w.publish(R,create_sensor_message().encode())
   H=time.time()
 except Exception as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

