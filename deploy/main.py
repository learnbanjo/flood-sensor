from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import MQTT_BROKER_ADD,MQTT_PUBLISH_INTERVAL,SPARKPLUGB_GID,SPARKPLUGB_EONID
from HW_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from utils import get_epoch_time
import json
import machine
import time
from umqtt.simple import MQTTClient
M="1.0"
n="spBv1.0/"+SPARKPLUGB_GID
v=n+"/DCMD"
h=n+"/DDATA/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
S=n+"/DBIRTH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
V=n+"/DDEATH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
I=5
X=-1 
p=1 
U=2 
x=DEVICE_NAME.encode()
O=", \"device_id\": \""+DEVICE_NAME+"\""
J=v.encode()
l=h.encode()
b=0
def reboot_with_reason(j,reason=0):
 d=get_sparkplug_prefx()+",\"ddeath_reasons\": \""+str(reason)+"\"}"
 j.publish(V.encode(),d.encode)
 j.disconnect()
 time.sleep(5)
 machine.reset() 
def get_sparkplug_prefx():
 global b
 if b>=2147483647:
  b=0
 b+=1
 return "{\"timestamp: \""+str(get_epoch_time())+O+",\"seq\": \""+str(b)+"\""
def sub_cb(topic,msg):
 if topic==J:
  z="\"device_id\":\""+DEVICE_NAME+"\""
  d=msg.decode()
  if(z in d or "\"device_id\":\"*\"" in d):
   if "\"cmdID\":\"OTA\"" in d:
    k=json.loads(d)
    from ota import OTAUpdater
    R="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
    D=k['payload'][0]['otafiles']
    r=True
    d=DEVICE_NAME+" OTA: "+D
    try:
     t=OTAUpdater(R,D)
     if t.check_for_updates():
      if t.download_and_install_update():
       d+=" updated"
      else:
       d+=" update failed"
     else:
      d+=" up-to-date" 
      r=False
    except Exception as C:
     d+=" err:"+str(C)+" type:"+str(type(C))
    finally:
     print(d)
     j.publish(h,d)
     if r:
      reboot_with_reason(j,U)
   elif "\"cmdID\":\"status\"" in d:
    j.publish(l,create_sensor_message())
   elif "\"cmdID\":\"reset\"" in d:
    reboot_with_reason(j,p)
def connect_and_subscribe():
 global x,J
 j=MQTTClient(x,MQTT_BROKER_ADD)
 j.set_callback(sub_cb)
 d=get_sparkplug_prefx()+",\"ddeath_reasons\": \"-1\"}"
 j.set_last_will(V,d.encode())
 j.connect()
 j.subscribe(J)
 B=get_sparkplug_prefx()+"}"
 j.publish(S.encode(),B.encode())
 return j
def restart_and_reconnect():
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global u
 global q
 d=get_sparkplug_prefx()+",\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(u!=""):
  d=d+",\"AnaR\":\""+str(u.read())+"\""
 if(q!=""):
  d=d+",\"DigR\":\""+str(q.value())+"\""
 if error!="":
  d=d+",\"err\":\""+error+"\""
 return d+"}"
u=""
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 u=ADC(ANALOG_SENSOR_PIN)
q=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 q=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
try:
 j=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
g=0
while True:
 try:
  j.check_msg()
  if(time.time()-g)>MQTT_PUBLISH_INTERVAL:
   j.publish(l,create_sensor_message().encode())
   g=time.time()
 except Exception as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

