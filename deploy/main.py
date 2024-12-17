from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import MQTT_BROKER_ADD,MQTT_PUBLISH_INTERVAL,SPARKPLUGB_GID,SPARKPLUGB_EONID
from HW_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from utils import get_epoch_time
import json
import machine
import time
from umqtt.simple import MQTTClient
H="1.0"
w="spBv1.0/"+SPARKPLUGB_GID
B=w+"/DCMD"
q=w+"/DDATA/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
v=w+"/DBIRTH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
N=w+"/DDEATH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
b=5
l=-1 
J=1 
T=2 
o=DEVICE_NAME.encode()
V=", \"device_id\": \""+DEVICE_NAME+"\""
m=B.encode()
e=q.encode()
i=0
def reboot_with_reason(p,reason=0):
 u=get_sparkplug_prefx()+",\"ddeath_reasons\": \""+str(reason)+"\"}"
 p.publish(N.encode(),u.encode)
 p.disconnect()
 time.sleep(5)
 machine.reset() 
def get_sparkplug_prefx():
 global i
 if i>=2147483647:
  i=0
 i+=1
 return "{\"timestamp: \""+str(get_epoch_time())+V+",\"seq\": \""+str(i)+"\""
def sub_cb(topic,msg):
 if topic==m:
  C="\"device_id\":\""+DEVICE_NAME+"\""
  u=msg.decode()
  if(C in u or "\"device_id\":\"*\"" in u):
   if "\"cmdID\":\"OTA\"" in u:
    U=json.loads(u)
    from ota import OTAUpdater
    L="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
    z=U['payload'][0]['otafiles']
    O=True
    u=DEVICE_NAME+" OTA: "+z
    try:
     A=OTAUpdater(L,z)
     if A.check_for_updates():
      if A.download_and_install_update():
       u+=" updated"
      else:
       u+=" update failed"
     else:
      u+=" up-to-date" 
      O=False
    except Exception as M:
     u+=" err:"+str(M)+" type:"+str(type(M))
    finally:
     print(u)
     p.publish(q,u)
     if O:
      reboot_with_reason(p,T)
   elif "\"cmdID\":\"status\"" in u:
    p.publish(e,create_sensor_message())
   elif "\"cmdID\":\"reset\"" in u:
    reboot_with_reason(p,J)
def connect_and_subscribe():
 global o,m
 p=MQTTClient(o,MQTT_BROKER_ADD)
 p.set_callback(sub_cb)
 u=get_sparkplug_prefx()+",\"ddeath_reasons\": \"-1\"}"
 p.set_last_will(N,u.encode())
 p.connect()
 p.subscribe(m)
 W=get_sparkplug_prefx()+"}"
 p.publish(v.encode(),W.encode())
 return p
def restart_and_reconnect():
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global g
 global h
 u=get_sparkplug_prefx()+",\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(g!=""):
  u=u+",\"AnaR\":\""+str(g.read())+"\""
 if(h!=""):
  u=u+",\"DigR\":\""+str(h.value())+"\""
 if error!="":
  u=u+",\"err\":\""+error+"\""
 return u+"}"
g=""
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 g=ADC(ANALOG_SENSOR_PIN)
h=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 h=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
try:
 p=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
G=0
while True:
 try:
  p.check_msg()
  if(time.time()-G)>MQTT_PUBLISH_INTERVAL:
   p.publish(e,create_sensor_message().encode())
   G=time.time()
 except Exception as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

