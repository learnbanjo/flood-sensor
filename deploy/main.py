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
E="1.0"
l="spBv1.0/"+SPARKPLUGB_GID
H=l+"/DCMD"
F=l+"/DDATA/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
q=l+"/DBIRTH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
P=l+"/DDEATH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
s=5
u=DEVICE_NAME.encode()
T=", \"device_id\": \""+DEVICE_NAME+"\""
O=H.encode()
k=F.encode()
R=0
def reboot_with_reason(I,reason=0):
 z=get_sparkplug_prefx()+",\"ddeath_reasons\": \""+str(reason)+"\"}"
 I.publish(P.encode(),z.encode)
 I.disconnect()
 time.sleep(5)
 machine.reset() 
def get_sparkplug_prefx():
 global R
 R+=1
 return "{\"timestamp: \""+str(get_epoch_time())+T+",\"seq\": \""+str(R)+"\""
def sub_cb(topic,msg):
 if topic==O:
  h="\"device_id\":\""+DEVICE_NAME+"\""
  z=msg.decode()
  if(h in z or "\"device_id\":\"*\"" in z):
   if "\"cmdID\":\"OTA\"" in z:
    y=json.loads(z)
    from ota import OTAUpdater
    Q="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
    Y=y['payload'][0]['otafiles']
    J=True
    z=DEVICE_NAME+" OTA: "+Y
    try:
     c=OTAUpdater(Q,Y)
     if c.check_for_updates():
      if c.download_and_install_update():
       z+=" updated"
      else:
       z+=" update failed"
     else:
      z+=" up-to-date" 
      J=False
    except Exception as p:
     z+=" err:"+str(p)+" type:"+str(type(p))
    finally:
     print(z)
     I.publish(F,z)
     if J:
      reboot_with_reason(I,DDEATH_REASON_OTA)
   elif "\"cmdID\":\"status\"" in z:
    I.publish(k,create_sensor_message())
   elif "\"cmdID\":\"reset\"" in z:
    reboot_with_reason(I,DDEATH_REASON_DCMD_REBOOT)
def connect_and_subscribe():
 global u,O
 I=MQTTClient(u,MQTT_BROKER_ADD)
 I.set_callback(sub_cb)
 z=get_sparkplug_prefx()+",\"ddeath_reasons\": \"-1\"}"
 I.set_last_will(P,z.encode())
 I.connect()
 I.subscribe(O)
 L=get_sparkplug_prefx()+"}"
 I.publish(q.encode(),L.encode())
 return I
def restart_and_reconnect():
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global i
 global e
 z=get_sparkplug_prefx()+",\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(i!=""):
  z=z+",\"AnaR\":\""+str(i.read())+"\""
 if(e!=""):
  z=z+",\"DigR\":\""+str(e.value())+"\""
 if error!="":
  z=z+",\"err\":\""+error+"\""
 return z+"}"
i=""
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 i=ADC(ANALOG_SENSOR_PIN)
e=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 e=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
try:
 I=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
X=0
while True:
 try:
  I.check_msg()
  if(time.time()-X)>MQTT_PUBLISH_INTERVAL:
   I.publish(k,create_sensor_message().encode())
   X=time.time()
 except Exception as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

