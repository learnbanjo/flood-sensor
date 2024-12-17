from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import MQTT_BROKER_ADD,MQTT_PUBLISH_INTERVAL,SPARKPLUGB_GID,SPARKPLUGB_EONID
from HW_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from utils import get_epoch_time
import json
import machine
import time
from umqtt.simple import MQTTClient
D="1.0"
t="spBv1.0/"+SPARKPLUGB_GID
M=t+"/DCMD"
R=t+"/DDATA/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
i=t+"/DBIRTH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
B=t+"/DDEATH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
K=5
L=-1 
V=1 
h=2 
T=DEVICE_NAME.encode()
g=", \"device_id\": \""+DEVICE_NAME+"\""
v=M.encode()
F=R.encode()
o=0
def reboot_with_reason(n,reason=0):
 G=get_sparkplug_prefx()+",\"ddeath_reasons\": \""+str(reason)+"\"}"
 n.publish(B.encode(),G.encode)
 n.disconnect()
 time.sleep(5)
 machine.reset() 
def get_sparkplug_prefx():
 global o
 if o>=2147483647:
  o=0
 o+=1
 return "{\"timestamp: \""+str(get_epoch_time())+g+",\"seq\": \""+str(o)+"\""
def sub_cb(topic,msg):
 if topic==v:
  E="\"device_id\":\""+DEVICE_NAME+"\""
  G=msg.decode()
  if(E in G or "\"device_id\":\"*\"" in G):
   if "\"cmdID\":\"OTA\"" in G:
    m=json.loads(G)
    from ota import OTAUpdater
    X="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
    p=m['payload'][0]['otafiles']
    S=True
    G=DEVICE_NAME+" OTA: "+p
    try:
     k=OTAUpdater(X,p)
     if k.check_for_updates():
      if k.download_and_install_update():
       G+=" updated"
      else:
       G+=" update failed"
     else:
      G+=" up-to-date" 
      S=False
    except Exception as U:
     G+=" err:"+str(U)+" type:"+str(type(U))
    finally:
     print(G)
     n.publish(R,G)
     if S:
      reboot_with_reason(n,h)
   elif "\"cmdID\":\"status\"" in G:
    n.publish(F,create_sensor_message())
   elif "\"cmdID\":\"reset\"" in G:
    reboot_with_reason(n,V)
def connect_and_subscribe():
 global T,v
 n=MQTTClient(T,MQTT_BROKER_ADD)
 n.set_callback(sub_cb)
 G=get_sparkplug_prefx()+",\"ddeath_reasons\": \"-1\"}"
 n.set_last_will(B,G.encode())
 n.connect()
 n.subscribe(v)
 a=get_sparkplug_prefx()+"}"
 n.publish(i.encode(),a.encode())
 return n
def restart_and_reconnect():
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global Q
 global C
 G=get_sparkplug_prefx()+",\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(Q!=""):
  G=G+",\"AnaR\":\""+str(Q.read())+"\""
 if(C!=""):
  G=G+",\"DigR\":\""+str(C.value())+"\""
 if error!="":
  G=G+",\"err\":\""+error+"\""
 return G+"}"
Q=""
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 Q=ADC(ANALOG_SENSOR_PIN)
C=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 C=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
try:
 n=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
I=0
while True:
 try:
  n.check_msg()
  if(time.time()-I)>MQTT_PUBLISH_INTERVAL:
   n.publish(F,create_sensor_message().encode())
   I=time.time()
 except Exception as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

