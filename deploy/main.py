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
I="1.0"
j="spBv1.0/"+SPARKPLUGB_GID
h=j+"/DCMD"
u=j+"/DDATA/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
t=j+"/DBIRTH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
v=j+"/DDEATH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
W=5
R=DEVICE_NAME.encode()
K=", \"device_id\": \""+DEVICE_NAME+"\""
z=h.encode()
i=u.encode()
P=0
def reboot_with_reason(F,reason=0):
 l=get_sparkplug_prefx()+",\"ddeath_reasons\": \""+str(reason)+"\"}"
 F.publish(v.encode(),l.encode)
 F.disconnect()
 time.sleep(5)
 machine.reset() 
def get_sparkplug_prefx():
 global P
 if P>=2147483647:
  P=0
 P+=1
 return "{\"timestamp: \""+str(get_epoch_time())+K+",\"seq\": \""+str(P)+"\""
def sub_cb(topic,msg):
 if topic==z:
  T="\"device_id\":\""+DEVICE_NAME+"\""
  l=msg.decode()
  if(T in l or "\"device_id\":\"*\"" in l):
   if "\"cmdID\":\"OTA\"" in l:
    n=json.loads(l)
    from ota import OTAUpdater
    y="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
    V=n['payload'][0]['otafiles']
    J=True
    l=DEVICE_NAME+" OTA: "+V
    try:
     d=OTAUpdater(y,V)
     if d.check_for_updates():
      if d.download_and_install_update():
       l+=" updated"
      else:
       l+=" update failed"
     else:
      l+=" up-to-date" 
      J=False
    except Exception as C:
     l+=" err:"+str(C)+" type:"+str(type(C))
    finally:
     print(l)
     F.publish(u,l)
     if J:
      reboot_with_reason(F,DDEATH_REASON_OTA)
   elif "\"cmdID\":\"status\"" in l:
    F.publish(i,create_sensor_message())
   elif "\"cmdID\":\"reset\"" in l:
    reboot_with_reason(F,DDEATH_REASON_DCMD_REBOOT)
def connect_and_subscribe():
 global R,z
 F=MQTTClient(R,MQTT_BROKER_ADD)
 F.set_callback(sub_cb)
 l=get_sparkplug_prefx()+",\"ddeath_reasons\": \"-1\"}"
 F.set_last_will(v,l.encode())
 F.connect()
 F.subscribe(z)
 r=get_sparkplug_prefx()+"}"
 F.publish(t.encode(),r.encode())
 return F
def restart_and_reconnect():
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global B
 global c
 l=get_sparkplug_prefx()+",\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(B!=""):
  l=l+",\"AnaR\":\""+str(B.read())+"\""
 if(c!=""):
  l=l+",\"DigR\":\""+str(c.value())+"\""
 if error!="":
  l=l+",\"err\":\""+error+"\""
 return l+"}"
B=""
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 B=ADC(ANALOG_SENSOR_PIN)
c=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 c=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
try:
 F=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
Y=0
while True:
 try:
  F.check_msg()
  if(time.time()-Y)>MQTT_PUBLISH_INTERVAL:
   F.publish(i,create_sensor_message().encode())
   Y=time.time()
 except Exception as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

