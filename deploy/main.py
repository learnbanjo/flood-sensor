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
f="1.0"
g="spBv1.0/"+SPARKPLUGB_GID
m=g+"/DCMD"
P=g+"/DDATA/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
R=g+"/DBIRTH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
y=g+"/DDEATH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
p=5
k=DEVICE_NAME.encode()
J=", \"device_id\": \""+DEVICE_NAME+"\""
v=m.encode()
z=P.encode()
F=0
def reboot_with_reason(O,reason=0):
 I=get_sparkplug_prefx()+",\"ddeath_reasons\": \""+str(reason)+"\"}"
 O.publish(y.encode(),I.encode)
 O.disconnect()
 time.sleep(5)
 machine.reset() 
def get_sparkplug_prefx():
 global F
 if F>=2147483647:
  F=0
 F+=1
 return "{\"timestamp: \""+str(get_epoch_time())+J+",\"seq\": \""+str(F)+"\""
def sub_cb(topic,msg):
 if topic==v:
  i="\"device_id\":\""+DEVICE_NAME+"\""
  I=msg.decode()
  if(i in I or "\"device_id\":\"*\"" in I):
   if "\"cmdID\":\"OTA\"" in I:
    q=json.loads(I)
    from ota import OTAUpdater
    T="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
    Y=q['payload'][0]['otafiles']
    c=True
    I=DEVICE_NAME+" OTA: "+Y
    try:
     N=OTAUpdater(T,Y)
     if N.check_for_updates():
      if N.download_and_install_update():
       I+=" updated"
      else:
       I+=" update failed"
     else:
      I+=" up-to-date" 
      c=False
    except Exception as S:
     I+=" err:"+str(S)+" type:"+str(type(S))
    finally:
     print(I)
     O.publish(P,I)
     if c:
      reboot_with_reason(O,DDEATH_REASON_OTA)
   elif "\"cmdID\":\"status\"" in I:
    O.publish(z,create_sensor_message())
   elif "\"cmdID\":\"reset\"" in I:
    reboot_with_reason(O,DDEATH_REASON_DCMD_REBOOT)
def connect_and_subscribe():
 global k,v
 O=MQTTClient(k,MQTT_BROKER_ADD)
 O.set_callback(sub_cb)
 I=get_sparkplug_prefx()+",\"ddeath_reasons\": \"-1\"}"
 O.set_last_will(y,I.encode())
 O.connect()
 O.subscribe(v)
 r=get_sparkplug_prefx()+"}"
 O.publish(R.encode(),r.encode())
 return O
def restart_and_reconnect():
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global G
 global s
 I=get_sparkplug_prefx()+",\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(G!=""):
  I=I+",\"AnaR\":\""+str(G.read())+"\""
 if(s!=""):
  I=I+",\"DigR\":\""+str(s.value())+"\""
 if error!="":
  I=I+",\"err\":\""+error+"\""
 return I+"}"
G=""
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 G=ADC(ANALOG_SENSOR_PIN)
s=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 s=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
try:
 O=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
B=0
while True:
 try:
  O.check_msg()
  if(time.time()-B)>MQTT_PUBLISH_INTERVAL:
   O.publish(z,create_sensor_message().encode())
   B=time.time()
 except Exception as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

