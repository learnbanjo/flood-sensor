from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import MQTT_BROKER_ADD,MQTT_PUBLISH_INTERVAL,SPARKPLUGB_GID,SPARKPLUGB_EONID
from HW_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from utils import get_epoch_time
import json
import machine
import time
from umqtt.simple import MQTTClient
T="1.0"
G="spBv1.0/"+SPARKPLUGB_GID
B=G+"/DCMD"
d=G+"/DDATA/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
u=G+"/DBIRTH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
h=G+"/DDEATH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
L=5
j=DEVICE_NAME.encode()
g=", \"device_id\": \""+DEVICE_NAME+"\""
E=B.encode()
I=d.encode()
S=0
def reboot_with_reason(q,reason=0):
 f=get_sparkplug_prefx()+",\"ddeath_reasons\": \""+str(reason)+"\"}"
 q.publish(h.encode(),f.encode)
 time.sleep(5)
def get_sparkplug_prefx():
 global S
 if S>=2147483647:
  S=0
 S+=1
 return "{\"timestamp: \""+str(get_epoch_time())+g+",\"seq\": \""+str(S)+"\""
def sub_cb(topic,msg):
 if topic==E:
  o="\"device_id\":\""+DEVICE_NAME+"\""
  f=msg.decode()
  if(o in f or "\"device_id\":\"*\"" in f):
   if "\"cmdID\":\"OTA\"" in f:
    A=json.loads(f)
    from ota import OTAUpdater
    H="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
    R=A['payload'][0]['otafiles']
    y=True
    f=DEVICE_NAME+" OTA: "+R
    try:
     C=OTAUpdater(H,R)
     if C.check_for_updates():
      if C.download_and_install_update():
       f+=" updated"
      else:
       f+=" update failed"
     else:
      f+=" up-to-date" 
      y=False
    except Exception as r:
     f+=" err:"+str(r)+" type:"+str(type(r))
    finally:
     print(f)
     q.publish(d,f)
     if y:
      reboot_with_reason(q,DDEATH_REASON_OTA)
   elif "\"cmdID\":\"status\"" in f:
    q.publish(I,create_sensor_message())
   elif "\"cmdID\":\"reset\"" in f:
    reboot_with_reason(q,DDEATH_REASON_DCMD_REBOOT)
def connect_and_subscribe():
 global j,E
 q=MQTTClient(j,MQTT_BROKER_ADD)
 q.set_callback(sub_cb)
 f=get_sparkplug_prefx()+",\"ddeath_reasons\": \"-1\"}"
 q.set_last_will(h,f.encode())
 q.connect()
 q.subscribe(E)
 q.publish(u.encode(),create_sensor_message().encode())
 return q
def restart_and_reconnect():
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global k
 global w
 f=get_sparkplug_prefx()+",\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(k!=""):
  f=f+",\"AnaR\":\""+str(k.read())+"\""
 if(w!=""):
  f=f+",\"DigR\":\""+str(w.value())+"\""
 if error!="":
  f=f+",\"err\":\""+error+"\""
 return f+"}"
k=""
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 k=ADC(ANALOG_SENSOR_PIN)
w=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 w=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
try:
 q=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
Y=0
while True:
 try:
  q.check_msg()
  if(time.time()-Y)>MQTT_PUBLISH_INTERVAL:
   q.publish(I,create_sensor_message().encode())
   Y=time.time()
 except Exception as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

