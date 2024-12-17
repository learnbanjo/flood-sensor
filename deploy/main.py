from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import MQTT_BROKER_ADD,MQTT_PUBLISH_INTERVAL,SPARKPLUGB_GID,SPARKPLUGB_EONID
from HW_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from utils import get_epoch_time
import json
import machine
import time
from umqtt.simple import MQTTClient
D="1.0"
A="spBv1.0/"+SPARKPLUGB_GID
T=A+"/DCMD"
J=A+"/DDATA/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
H=A+"/DBIRTH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
p=A+"/DDEATH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
l=5
y=-1 
w=1 
i=2 
F=DEVICE_NAME.encode()
W=", \"device_id\": \""+DEVICE_NAME+"\""
r=T.encode()
N=J.encode()
R=0
def reboot_with_reason(z,reason=0):
 j=get_sparkplug_prefx()+",\"ddeath_reasons\": \""+str(reason)+"\"}"
 z.publish(p.encode(),j.encode)
 z.disconnect()
 time.sleep(5)
 machine.reset() 
def get_sparkplug_prefx():
 global R
 if R>=2147483647:
  R=0
 R+=1
 return "{\"timestamp: \""+str(get_epoch_time())+W+",\"seq\": \""+str(R)+"\""
def sub_cb(topic,msg):
 if topic==r:
  K="\"device_id\":\""+DEVICE_NAME+"\""
  j=msg.decode()
  if(K in j or "\"device_id\":\"*\"" in j):
   if "\"cmdID\":\"OTA\"" in j:
    c=json.loads(j)
    from ota import OTAUpdater
    n="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
    C=c['payload'][0]['otafiles']
    a=True
    j=DEVICE_NAME+" OTA: "+C
    try:
     k=OTAUpdater(n,C)
     if k.check_for_updates():
      if k.download_and_install_update():
       j+=" updated"
      else:
       j+=" update failed"
     else:
      j+=" up-to-date" 
      a=False
    except Exception as m:
     j+=" err:"+str(m)+" type:"+str(type(m))
    finally:
     print(j)
     z.publish(J,j)
     if a:
      reboot_with_reason(z,i)
   elif "\"cmdID\":\"status\"" in j:
    z.publish(N,create_sensor_message())
   elif "\"cmdID\":\"reset\"" in j:
    reboot_with_reason(z,w)
def connect_and_subscribe():
 global F,r
 z=MQTTClient(F,MQTT_BROKER_ADD)
 z.set_callback(sub_cb)
 j=get_sparkplug_prefx()+",\"ddeath_reasons\": \"-1\"}"
 z.set_last_will(p,j.encode())
 z.connect()
 z.subscribe(r)
 d=get_sparkplug_prefx()+"}"
 z.publish(H.encode(),d.encode())
 return z
def restart_and_reconnect():
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global Y
 global E
 j=get_sparkplug_prefx()+",\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(Y!=""):
  j=j+",\"AnaR\":\""+str(Y.read())+"\""
 if(E!=""):
  j=j+",\"DigR\":\""+str(E.value())+"\""
 if error!="":
  j=j+",\"err\":\""+error+"\""
 return j+"}"
Y=""
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 Y=ADC(ANALOG_SENSOR_PIN)
E=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 E=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
try:
 z=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
e=0
while True:
 try:
  z.check_msg()
  if(time.time()-e)>MQTT_PUBLISH_INTERVAL:
   z.publish(N,create_sensor_message().encode())
   e=time.time()
 except Exception as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

