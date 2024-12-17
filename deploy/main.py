from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import MQTT_BROKER_ADD,MQTT_PUBLISH_INTERVAL,SPARKPLUGB_GID,SPARKPLUGB_EONID
from HW_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from utils import get_epoch_time
import json
import machine
import time
from umqtt.simple import MQTTClient
U="1.0"
d="spBv1.0/"+SPARKPLUGB_GID
w=d+"/DCMD"
a=d+"/DDATA/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
A=d+"/DBIRTH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
t=d+"/DDEATH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
S=5
T=DEVICE_NAME.encode()
g=", \"device_id\": \""+DEVICE_NAME+"\""
r=w.encode()
b=a.encode()
H=0
def reboot_with_reason(D,reason=0):
 p=get_sparkplug_prefx()+",\"ddeath_reasons\": \""+str(reason)+"\"}"
 D.publish(t.encode(),p.encode)
 D.disconnect()
 time.sleep(5)
 machine.reset() 
def get_sparkplug_prefx():
 global H
 if H>=2147483647:
  H=0
 H+=1
 return "{\"timestamp: \""+str(get_epoch_time())+g+",\"seq\": \""+str(H)+"\""
def sub_cb(topic,msg):
 if topic==r:
  y="\"device_id\":\""+DEVICE_NAME+"\""
  p=msg.decode()
  if(y in p or "\"device_id\":\"*\"" in p):
   if "\"cmdID\":\"OTA\"" in p:
    q=json.loads(p)
    from ota import OTAUpdater
    M="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
    C=q['payload'][0]['otafiles']
    J=True
    p=DEVICE_NAME+" OTA: "+C
    try:
     G=OTAUpdater(M,C)
     if G.check_for_updates():
      if G.download_and_install_update():
       p+=" updated"
      else:
       p+=" update failed"
     else:
      p+=" up-to-date" 
      J=False
    except Exception as B:
     p+=" err:"+str(B)+" type:"+str(type(B))
    finally:
     print(p)
     D.publish(a,p)
     if J:
      reboot_with_reason(D,DDEATH_REASON_OTA)
   elif "\"cmdID\":\"status\"" in p:
    D.publish(b,create_sensor_message())
   elif "\"cmdID\":\"reset\"" in p:
    reboot_with_reason(D,DDEATH_REASON_DCMD_REBOOT)
def connect_and_subscribe():
 global T,r
 D=MQTTClient(T,MQTT_BROKER_ADD)
 D.set_callback(sub_cb)
 p=get_sparkplug_prefx()+",\"ddeath_reasons\": \"-1\"}"
 D.set_last_will(t,p.encode())
 D.connect()
 D.subscribe(r)
 D.publish(A.encode(),create_sensor_message().encode())
 return D
def restart_and_reconnect():
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global Y
 global Q
 p=get_sparkplug_prefx()+",\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(Y!=""):
  p=p+",\"AnaR\":\""+str(Y.read())+"\""
 if(Q!=""):
  p=p+",\"DigR\":\""+str(Q.value())+"\""
 if error!="":
  p=p+",\"err\":\""+error+"\""
 return p+"}"
Y=""
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 Y=ADC(ANALOG_SENSOR_PIN)
Q=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 Q=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
try:
 D=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
L=0
while True:
 try:
  D.check_msg()
  if(time.time()-L)>MQTT_PUBLISH_INTERVAL:
   D.publish(b,create_sensor_message().encode())
   L=time.time()
 except Exception as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

