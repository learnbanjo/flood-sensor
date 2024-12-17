from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import MQTT_BROKER_ADD,MQTT_PUBLISH_INTERVAL,SPARKPLUGB_GID,SPARKPLUGB_EONID
from HW_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from utils import get_epoch_time
import json
import machine
import time
from umqtt.simple import MQTTClient
h="1.0"
f="spBv1.0/"+SPARKPLUGB_GID
S=f+"/DCMD"
c=f+"/DDATA/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
P=f+"/DBIRTH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
q=f+"/DDEATH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
B=5
z=DEVICE_NAME.encode()
u=", \"device_id\": \""+DEVICE_NAME+"\""
D=S.encode()
v=c.encode()
e=0
def reboot_with_reason(r,reason=0):
 i=get_sparkplug_prefx()+",\"ddeath_reasons\": \""+str(reason)+"\"}"
 r.publish(q.encode(),i.encode)
 r.disconnect()
 time.sleep(5)
 machine.reset() 
def get_sparkplug_prefx():
 global e
 if e>=2147483647:
  e=0
 e+=1
 return "{\"timestamp: \""+str(get_epoch_time())+u+",\"seq\": \""+str(e)+"\""
def sub_cb(topic,msg):
 if topic==D:
  Y="\"device_id\":\""+DEVICE_NAME+"\""
  i=msg.decode()
  if(Y in i or "\"device_id\":\"*\"" in i):
   if "\"cmdID\":\"OTA\"" in i:
    R=json.loads(i)
    from ota import OTAUpdater
    d="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
    T=R['payload'][0]['otafiles']
    E=True
    i=DEVICE_NAME+" OTA: "+T
    try:
     U=OTAUpdater(d,T)
     if U.check_for_updates():
      if U.download_and_install_update():
       i+=" updated"
      else:
       i+=" update failed"
     else:
      i+=" up-to-date" 
      E=False
    except Exception as A:
     i+=" err:"+str(A)+" type:"+str(type(A))
    finally:
     print(i)
     r.publish(c,i)
     if E:
      reboot_with_reason(r,DDEATH_REASON_OTA)
   elif "\"cmdID\":\"status\"" in i:
    r.publish(v,create_sensor_message())
   elif "\"cmdID\":\"reset\"" in i:
    reboot_with_reason(r,DDEATH_REASON_DCMD_REBOOT)
def connect_and_subscribe():
 global z,D
 r=MQTTClient(z,MQTT_BROKER_ADD)
 r.set_callback(sub_cb)
 i=get_sparkplug_prefx()+",\"ddeath_reasons\": \"-1\"}"
 r.set_last_will(q,i.encode())
 r.connect()
 r.subscribe(D)
 V=get_sparkplug_prefx()+"}"
 r.publish(P.encode(),V.encode())
 return r
def restart_and_reconnect():
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global m
 global k
 i=get_sparkplug_prefx()+",\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(m!=""):
  i=i+",\"AnaR\":\""+str(m.read())+"\""
 if(k!=""):
  i=i+",\"DigR\":\""+str(k.value())+"\""
 if error!="":
  i=i+",\"err\":\""+error+"\""
 return i+"}"
m=""
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 m=ADC(ANALOG_SENSOR_PIN)
k=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 k=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
try:
 r=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
W=0
while True:
 try:
  r.check_msg()
  if(time.time()-W)>MQTT_PUBLISH_INTERVAL:
   r.publish(v,create_sensor_message().encode())
   W=time.time()
 except Exception as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

