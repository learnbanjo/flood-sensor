from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import MQTT_BROKER_ADD,MQTT_PUBLISH_INTERVAL,SPARKPLUGB_GID,SPARKPLUGB_EONID
from HW_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from utils import get_epoch_time
import json
import machine
import time
from umqtt.simple import MQTTClient
B="1.0"
j="spBv1.0/"+SPARKPLUGB_GID
O=j+"/DCMD"
J=j+"/DDATA/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
H=j+"/DBIRTH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
Q=j+"/DDEATH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
S=5
e=-1 
F=1 
l=2 
U=DEVICE_NAME.encode()
D=", \"device_id\": \""+DEVICE_NAME+"\""
p=O.encode()
h=J.encode()
X=0
def reboot_with_reason(f,reason=0):
 W=get_sparkplug_prefx()+",\"ddeath_reasons\": \""+str(reason)+"\"}"
 f.publish(Q.encode(),W.encode)
 f.disconnect()
 time.sleep(5)
 machine.reset() 
def get_sparkplug_prefx():
 global X
 if X>=2147483647:
  X=0
 X+=1
 return "{\"timestamp: \""+str(get_epoch_time())+D+",\"seq\": \""+str(X)+"\""
def sub_cb(topic,msg):
 if topic==p:
  T="\"device_id\":\""+DEVICE_NAME+"\""
  W=msg.decode()
  if(T in W or "\"device_id\":\"*\"" in W):
   if "\"cmdID\":\"OTA\"" in W:
    c=json.loads(W)
    from ota import OTAUpdater
    R="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
    C=c['payload'][0]['otafiles']
    K=True
    W=DEVICE_NAME+" OTA: "+C
    try:
     L=OTAUpdater(R,C)
     if L.check_for_updates():
      if L.download_and_install_update():
       W+=" updated"
      else:
       W+=" update failed"
     else:
      W+=" up-to-date" 
      K=False
    except Exception as x:
     W+=" err:"+str(x)+" type:"+str(type(x))
    finally:
     print(W)
     f.publish(J,W)
     if K:
      reboot_with_reason(f,l)
   elif "\"cmdID\":\"status\"" in W:
    f.publish(h,create_sensor_message())
   elif "\"cmdID\":\"reset\"" in W:
    reboot_with_reason(f,F)
def connect_and_subscribe():
 global U,p
 f=MQTTClient(U,MQTT_BROKER_ADD)
 f.set_callback(sub_cb)
 W=get_sparkplug_prefx()+",\"ddeath_reasons\": \"-1\"}"
 f.set_last_will(Q,W.encode())
 f.connect()
 f.subscribe(p)
 s=get_sparkplug_prefx()+"}"
 f.publish(H.encode(),s.encode())
 return f
def restart_and_reconnect():
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global g
 global b
 W=get_sparkplug_prefx()+",\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(g!=""):
  W=W+",\"AnaR\":\""+str(g.read())+"\""
 if(b!=""):
  W=W+",\"DigR\":\""+str(b.value())+"\""
 if error!="":
  W=W+",\"err\":\""+error+"\""
 return W+"}"
g=""
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 g=ADC(ANALOG_SENSOR_PIN)
b=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 b=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
try:
 f=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
a=0
while True:
 try:
  f.check_msg()
  if(time.time()-a)>MQTT_PUBLISH_INTERVAL:
   f.publish(h,create_sensor_message().encode())
   a=time.time()
 except Exception as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

