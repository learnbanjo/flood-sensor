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
j="1.0"
H="spBv1.0/"+SPARKPLUGB_GID
l=H+"/DCMD"
K=H+"/DDATA/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
Q=H+"/DBIRTH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
m=H+"/DDEATH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
h=5
u=DEVICE_NAME.encode()
r=", \"device_id\": \""+DEVICE_NAME+"\""
q=l.encode()
U=K.encode()
c=0
def reboot_with_reason(w,reason=0):
 L=get_sparkplug_prefx()+",\"ddeath_reasons\": \""+str(reason)+"\"}"
 w.publish(m.encode(),L.encode)
 w.disconnect()
 time.sleep(5)
 machine.reset() 
def get_sparkplug_prefx():
 global c
 c+=1
 return "{\"timestamp: \""+str(get_epoch_time())+r+",\"seq\": \""+str(c)+"\""
def sub_cb(topic,msg):
 if topic==q:
  s="\"device_id\":\""+DEVICE_NAME+"\""
  L=msg.decode()
  if(s in L or "\"device_id\":\"*\"" in L):
   if "\"cmdID\":\"OTA\"" in L:
    I=json.loads(L)
    from ota import OTAUpdater
    A="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
    e=I['payload'][0]['otafiles']
    a=True
    L=DEVICE_NAME+" OTA: "+e
    try:
     F=OTAUpdater(A,e)
     if F.check_for_updates():
      if F.download_and_install_update():
       L+=" updated"
      else:
       L+=" update failed"
     else:
      L+=" up-to-date" 
      a=False
    except Exception as Y:
     L+=" err:"+str(Y)+" type:"+str(type(Y))
    finally:
     print(L)
     w.publish(K,L)
     if a:
      reboot_with_reason(w,DDEATH_REASON_OTA)
   elif "\"cmdID\":\"status\"" in L:
    w.publish(U,create_sensor_message())
   elif "\"cmdID\":\"reset\"" in L:
    reboot_with_reason(w,DDEATH_REASON_DCMD_REBOOT)
def connect_and_subscribe():
 global u,q
 w=MQTTClient(u,MQTT_BROKER_ADD)
 w.set_callback(sub_cb)
 L=get_sparkplug_prefx()+",\"ddeath_reasons\": \"-1\"}"
 w.set_last_will(m,L.encode())
 w.connect()
 w.subscribe(q)
 T=get_sparkplug_prefx()+"}"
 w.publish(Q.encode(),T.encode())
 return w
def restart_and_reconnect():
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global D
 global y
 L=get_sparkplug_prefx()+",\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(D!=""):
  L=L+",\"AnaR\":\""+str(D.read())+"\""
 if(y!=""):
  L=L+",\"DigR\":\""+str(y.value())+"\""
 if error!="":
  L=L+",\"err\":\""+error+"\""
 return L+"}"
D=""
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 D=ADC(ANALOG_SENSOR_PIN)
y=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 y=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
try:
 w=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
k=0
while True:
 try:
  w.check_msg()
  if(time.time()-k)>MQTT_PUBLISH_INTERVAL:
   w.publish(U,create_sensor_message().encode())
   k=time.time()
 except Exception as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

