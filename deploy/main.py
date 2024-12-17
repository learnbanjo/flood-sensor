from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import MQTT_BROKER_ADD,MQTT_PUBLISH_INTERVAL,SPARKPLUGB_GID,SPARKPLUGB_EONID
from HW_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from utils import get_epoch_time
import json
import machine
import time
from umqtt.simple import MQTTClient
r="1.0"
G="spBv1.0/"+SPARKPLUGB_GID
f=G+"/DCMD"
c=G+"/DDATA/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
T=G+"/DBIRTH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
J=G+"/DDEATH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
n=5
L=DEVICE_NAME.encode()
D=", \"device_id\": \""+DEVICE_NAME+"\""
X=f.encode()
Y=c.encode()
u=0
def reboot_with_reason(O,reason=0):
 B=get_sparkplug_prefx()+",\"ddeath_reasons\": \""+str(reason)+"\"}"
 O.publish(J.encode(),B.encode)
 time.sleep(5)
def get_sparkplug_prefx():
 global u
 if u>=2147483647:
  u=0
 u+=1
 return "{\"timestamp: \""+str(get_epoch_time())+D+",\"seq\": \""+str(u)+"\""
def sub_cb(topic,msg):
 if topic==X:
  H="\"device_id\":\""+DEVICE_NAME+"\""
  B=msg.decode()
  if(H in B or "\"device_id\":\"*\"" in B):
   if "\"cmdID\":\"OTA\"" in B:
    v=json.loads(B)
    from ota import OTAUpdater
    w="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
    Q=v['payload'][0]['otafiles']
    e=True
    B=DEVICE_NAME+" OTA: "+Q
    try:
     C=OTAUpdater(w,Q)
     if C.check_for_updates():
      if C.download_and_install_update():
       B+=" updated"
      else:
       B+=" update failed"
     else:
      B+=" up-to-date" 
      e=False
    except Exception as S:
     B+=" err:"+str(S)+" type:"+str(type(S))
    finally:
     print(B)
     O.publish(c,B)
     if e:
      reboot_with_reason(O,DDEATH_REASON_OTA)
   elif "\"cmdID\":\"status\"" in B:
    O.publish(Y,create_sensor_message())
   elif "\"cmdID\":\"reset\"" in B:
    reboot_with_reason(O,DDEATH_REASON_DCMD_REBOOT)
def connect_and_subscribe():
 global L,X
 O=MQTTClient(L,MQTT_BROKER_ADD)
 O.set_callback(sub_cb)
 B=get_sparkplug_prefx()+",\"ddeath_reasons\": \"-1\"}"
 O.set_last_will(J,B.encode())
 O.connect()
 O.subscribe(X)
 O.publish(T.encode(),create_sensor_message().encode())
 return O
def restart_and_reconnect():
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global k
 global V
 B=get_sparkplug_prefx()+",\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(k!=""):
  B=B+",\"AnaR\":\""+str(k.read())+"\""
 if(V!=""):
  B=B+",\"DigR\":\""+str(V.value())+"\""
 if error!="":
  B=B+",\"err\":\""+error+"\""
 return B+"}"
k=""
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 k=ADC(ANALOG_SENSOR_PIN)
V=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 V=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
try:
 O=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
x=0
while True:
 try:
  O.check_msg()
  if(time.time()-x)>MQTT_PUBLISH_INTERVAL:
   O.publish(Y,create_sensor_message().encode())
   x=time.time()
 except Exception as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

