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
p="1.0"
A="spBv1.0/"+SPARKPLUGB_GID
o=A+"/DCMD"
x=A+"/DDATA/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
Y=A+"/DBIRTH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
y=A+"/DDEATH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
u=5
m=DEVICE_NAME.encode()
C=", \"device_id\": \""+DEVICE_NAME+"\""
N=o.encode()
b=x.encode()
G=0
def reboot_with_reason(d,reason=0):
 l=get_sparkplug_prefx()+",\"ddeath_reasons\": \""+str(reason)+"\"}"
 d.publish(y.encode(),l.encode)
 d.disconnect()
 time.sleep(5)
 machine.reset() 
def get_sparkplug_prefx():
 global G
 G+=1
 return "{\"timestamp: \""+str(get_epoch_time())+C+",\"seq\": \""+str(G)+"\""
def sub_cb(topic,msg):
 if topic==N:
  D="\"device_id\":\""+DEVICE_NAME+"\""
  l=msg.decode()
  if(D in l or "\"device_id\":\"*\"" in l):
   if "\"cmdID\":\"OTA\"" in l:
    U=json.loads(l)
    from ota import OTAUpdater
    Q="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
    f=U['payload'][0]['otafiles']
    M=True
    l=DEVICE_NAME+" OTA: "+f
    try:
     K=OTAUpdater(Q,f)
     if K.check_for_updates():
      if K.download_and_install_update():
       l+=" updated"
      else:
       l+=" update failed"
     else:
      l+=" up-to-date" 
      M=False
    except Exception as c:
     l+=" err:"+str(c)+" type:"+str(type(c))
    finally:
     print(l)
     d.publish(x,l)
     if M:
      reboot_with_reason(d,DDEATH_REASON_OTA)
   elif "\"cmdID\":\"status\"" in l:
    d.publish(b,create_sensor_message())
   elif "\"cmdID\":\"reset\"" in l:
    reboot_with_reason(d,DDEATH_REASON_DCMD_REBOOT)
def connect_and_subscribe():
 global m,N
 d=MQTTClient(m,MQTT_BROKER_ADD)
 d.set_callback(sub_cb)
 l=get_sparkplug_prefx()+",\"ddeath_reasons\": \"-1\"}"
 d.set_last_will(y,l.encode())
 d.connect()
 d.subscribe(N)
 i=get_sparkplug_prefx()+"}"
 d.publish(Y.encode(),i.encode())
 return d
def restart_and_reconnect():
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global F
 global J
 l=get_sparkplug_prefx()+",\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(F!=""):
  l=l+",\"AnaR\":\""+str(F.read())+"\""
 if(J!=""):
  l=l+",\"DigR\":\""+str(J.value())+"\""
 if error!="":
  l=l+",\"err\":\""+error+"\""
 return l+"}"
F=""
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 F=ADC(ANALOG_SENSOR_PIN)
J=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 J=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
try:
 d=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
W=0
while True:
 try:
  d.check_msg()
  if(time.time()-W)>MQTT_PUBLISH_INTERVAL:
   d.publish(b,create_sensor_message().encode())
   W=time.time()
 except Exception as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

