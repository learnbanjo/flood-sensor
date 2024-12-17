from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import MQTT_BROKER_ADD,MQTT_PUBLISH_INTERVAL,SPARKPLUGB_GID,SPARKPLUGB_EONID
from HW_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from utils import get_epoch_time
import json
import machine
import time
from umqtt.simple import MQTTClient
n="1.0"
a="spBv1.0/"+SPARKPLUGB_GID
E=a+"/DCMD"
N=a+"/DDATA/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
c=a+"/DBIRTH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
u=a+"/DDEATH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
k=5
q=DEVICE_NAME.encode()
e=", \"device_id\": \""+DEVICE_NAME+"\""
J=E.encode()
I=N.encode()
o=0
def reboot_with_reason(U,reason=0):
 T=get_sparkplug_prefx()+",\"ddeath_reasons\": \""+str(reason)+"\"}"
 U.publish(u.encode(),T.encode)
 time.sleep(5)
def get_sparkplug_prefx():
 global o
 if o>=2147483647:
  o=0
 o+=1
 return "{\"timestamp: \""+str(get_epoch_time())+e+",\"seq\": \""+str(o)+"\""
def sub_cb(topic,msg):
 if topic==J:
  r="\"device_id\":\""+DEVICE_NAME+"\""
  T=msg.decode()
  if(r in T or "\"device_id\":\"*\"" in T):
   if "\"cmdID\":\"OTA\"" in T:
    W=json.loads(T)
    from ota import OTAUpdater
    m="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
    v=W['payload'][0]['otafiles']
    Q=True
    T=DEVICE_NAME+" OTA: "+v
    try:
     O=OTAUpdater(m,v)
     if O.check_for_updates():
      if O.download_and_install_update():
       T+=" updated"
      else:
       T+=" update failed"
     else:
      T+=" up-to-date" 
      Q=False
    except Exception as L:
     T+=" err:"+str(L)+" type:"+str(type(L))
    finally:
     print(T)
     U.publish(N,T)
     if Q:
      reboot_with_reason(U,DDEATH_REASON_OTA)
   elif "\"cmdID\":\"status\"" in T:
    U.publish(I,create_sensor_message())
   elif "\"cmdID\":\"reset\"" in T:
    reboot_with_reason(U,DDEATH_REASON_DCMD_REBOOT)
def connect_and_subscribe():
 global q,J
 U=MQTTClient(q,MQTT_BROKER_ADD)
 U.set_callback(sub_cb)
 T=get_sparkplug_prefx()+",\"ddeath_reasons\": \"-1\"}"
 U.set_last_will(u,T.encode())
 U.connect()
 U.subscribe(J)
 U.publish(c.encode(),create_sensor_message().encode())
 return U
def restart_and_reconnect():
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global R
 global l
 T=get_sparkplug_prefx()+",\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(R!=""):
  T=T+",\"AnaR\":\""+str(R.read())+"\""
 if(l!=""):
  T=T+",\"DigR\":\""+str(l.value())+"\""
 if error!="":
  T=T+",\"err\":\""+error+"\""
 return T+"}"
R=""
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 R=ADC(ANALOG_SENSOR_PIN)
l=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 l=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
try:
 U=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
f=0
while True:
 try:
  U.check_msg()
  if(time.time()-f)>MQTT_PUBLISH_INTERVAL:
   U.publish(I,create_sensor_message().encode())
   f=time.time()
 except Exception as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

