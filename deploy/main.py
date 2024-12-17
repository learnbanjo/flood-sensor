from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import MQTT_BROKER_ADD,MQTT_PUBLISH_INTERVAL,SPARKPLUGB_GID,SPARKPLUGB_EONID
from HW_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from utils import get_epoch_time
import json
import machine
import time
from umqtt.simple import MQTTClient
A="1.0"
S="spBv1.0/"+SPARKPLUGB_GID
D=S+"/DCMD"
R=S+"/DDATA/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
n=S+"/DBIRTH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
x=S+"/DDEATH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
L=5
p=-1 
l=1 
t=2 
I=DEVICE_NAME.encode()
U=", \"device_id\": \""+DEVICE_NAME+"\""
f=D.encode()
J=R.encode()
X=0
def reboot_with_reason(r,reason=0):
 e=get_sparkplug_prefx()+",\"ddeath_reasons\": \""+str(reason)+"\"}"
 r.publish(x.encode(),e.encode)
 r.disconnect()
 time.sleep(5)
 machine.reset() 
def get_sparkplug_prefx():
 global X
 if X>=2147483647:
  X=0
 X+=1
 return "{\"timestamp: \""+str(get_epoch_time())+U+",\"seq\": \""+str(X)+"\""
def sub_cb(topic,msg):
 if topic==f:
  o="\"device_id\":\""+DEVICE_NAME+"\""
  e=msg.decode()
  if(o in e or "\"device_id\":\"*\"" in e):
   if "\"cmdID\":\"OTA\"" in e:
    q=json.loads(e)
    from ota import OTAUpdater
    G="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
    d=q['payload'][0]['otafiles']
    W=True
    e=DEVICE_NAME+" OTA: "+d
    try:
     Q=OTAUpdater(G,d)
     if Q.check_for_updates():
      if Q.download_and_install_update():
       e+=" updated"
      else:
       e+=" update failed"
     else:
      e+=" up-to-date" 
      W=False
    except Exception as w:
     e+=" err:"+str(w)+" type:"+str(type(w))
    finally:
     print(e)
     r.publish(R,e)
     if W:
      reboot_with_reason(r,t)
   elif "\"cmdID\":\"status\"" in e:
    r.publish(J,create_sensor_message())
   elif "\"cmdID\":\"reset\"" in e:
    reboot_with_reason(r,l)
def connect_and_subscribe():
 global I,f
 r=MQTTClient(I,MQTT_BROKER_ADD)
 r.set_callback(sub_cb)
 e=get_sparkplug_prefx()+",\"ddeath_reasons\": \"-1\"}"
 r.set_last_will(x,e.encode())
 r.connect()
 r.subscribe(f)
 k=get_sparkplug_prefx()+"}"
 r.publish(n.encode(),k.encode())
 return r
def restart_and_reconnect():
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global i
 global H
 e=get_sparkplug_prefx()+",\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(i!=""):
  e=e+",\"AnaR\":\""+str(i.read())+"\""
 if(H!=""):
  e=e+",\"DigR\":\""+str(H.value())+"\""
 if error!="":
  e=e+",\"err\":\""+error+"\""
 return e+"}"
i=""
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 i=ADC(ANALOG_SENSOR_PIN)
H=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 H=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
try:
 r=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
V=0
while True:
 try:
  r.check_msg()
  if(time.time()-V)>MQTT_PUBLISH_INTERVAL:
   r.publish(J,create_sensor_message().encode())
   V=time.time()
 except Exception as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

