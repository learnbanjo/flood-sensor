from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import MQTT_BROKER_ADD,MQTT_PUBLISH_INTERVAL,SPARKPLUGB_GID,SPARKPLUGB_EONID
from HW_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from utils import get_epoch_time
import json
import machine
import time
from umqtt.simple import MQTTClient
C="1.0"
y="spBv1.0/"+SPARKPLUGB_GID
l=y+"/DCMD"
n=y+"/DDATA/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
F=y+"/DBIRTH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
Y=y+"/DDEATH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
L=5
Q=-1 
X=1 
a=2 
P=DEVICE_NAME.encode()
b=l.encode()
h=n.encode()
E=0
def reboot_with_reason(m,reason=0):
 d=get_sparkplug_prefx()+",\"ddeath_reasons\": \""+str(reason)+"\"}"
 m.publish(Y.encode(),d.encode)
 m.disconnect()
 time.sleep(5)
 machine.reset() 
def get_sparkplug_prefx():
 global E
 if E>=2147483647:
  E=0
 E+=1
 return "{\"timestamp\": \""+str(get_epoch_time())+"\", \"device_id\": \""+DEVICE_NAME+"\",\"seq\": \""+str(E)+"\""
def sub_cb(topic,msg):
 if topic==b:
  H="\"device_id\":\""+DEVICE_NAME+"\""
  d=msg.decode()
  if(H in d or "\"device_id\":\"*\"" in d):
   if "\"cmdID\":\"OTA\"" in d:
    B=json.loads(d)
    from ota import OTAUpdater
    O="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
    J=B['payload'][0]['otafiles']
    f=True
    d=DEVICE_NAME+" OTA: "+J
    try:
     S=OTAUpdater(O,J)
     if S.check_for_updates():
      if S.download_and_install_update():
       d+=" updated"
      else:
       d+=" update failed"
     else:
      d+=" up-to-date" 
      f=False
    except Exception as p:
     d+=" err:"+str(p)+" type:"+str(type(p))
    finally:
     print(d)
     m.publish(n,d)
     if f:
      reboot_with_reason(m,a)
   elif "\"cmdID\":\"status\"" in d:
    m.publish(h,create_sensor_message())
   elif "\"cmdID\":\"reset\"" in d:
    reboot_with_reason(m,X)
def connect_and_subscribe():
 global P,b
 m=MQTTClient(P,MQTT_BROKER_ADD)
 m.set_callback(sub_cb)
 d=get_sparkplug_prefx()+",\"ddeath_reasons\": \"-1\"}"
 m.set_last_will(Y,d.encode())
 m.connect()
 m.subscribe(b)
 i=get_sparkplug_prefx()+"}"
 m.publish(F.encode(),i.encode())
 return m
def restart_and_reconnect():
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global x
 global z
 d=get_sparkplug_prefx()+",\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(x!=""):
  d=d+",\"AnaR\":\""+str(x.read())+"\""
 if(z!=""):
  d=d+",\"DigR\":\""+str(z.value())+"\""
 if error!="":
  d=d+",\"err\":\""+error+"\""
 return d+"}"
x=""
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 x=ADC(ANALOG_SENSOR_PIN)
z=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 z=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
try:
 m=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
o=0
while True:
 try:
  m.check_msg()
  if(time.time()-o)>MQTT_PUBLISH_INTERVAL:
   m.publish(h,create_sensor_message().encode())
   o=time.time()
 except Exception as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

