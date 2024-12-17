from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import MQTT_BROKER_ADD,MQTT_PUBLISH_INTERVAL,SPARKPLUGB_GID,SPARKPLUGB_EONID
from HW_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from utils import get_epoch_time
import json
import machine
import time
from umqtt.simple import MQTTClient
v="1.0"
K="spBv1.0/"+SPARKPLUGB_GID
A=K+"/DCMD"
u=K+"/DDATA/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
n=K+"/DBIRTH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
z=K+"/DDEATH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
i=5
a=DEVICE_NAME.encode()
I=", \"device_id\": \""+DEVICE_NAME+"\""
l=A.encode()
O=u.encode()
h=0
def reboot_with_reason(p,reason=0):
 m=get_sparkplug_prefx()+",\"ddeath_reasons\": \""+str(reason)+"\"}"
 p.publish(z.encode(),m.encode)
 time.sleep(5)
def get_sparkplug_prefx():
 global h
 if h>=2147483647:
  h=0
 h+=1
 return "{\"timestamp: \""+str(get_epoch_time())+I+",\"seq\": \""+str(h)+"\""
def sub_cb(topic,msg):
 if topic==l:
  S="\"device_id\":\""+DEVICE_NAME+"\""
  m=msg.decode()
  if(S in m or "\"device_id\":\"*\"" in m):
   if "\"cmdID\":\"OTA\"" in m:
    y=json.loads(m)
    from ota import OTAUpdater
    j="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
    q=y['payload'][0]['otafiles']
    x=True
    m=DEVICE_NAME+" OTA: "+q
    try:
     D=OTAUpdater(j,q)
     if D.check_for_updates():
      if D.download_and_install_update():
       m+=" updated"
      else:
       m+=" update failed"
     else:
      m+=" up-to-date" 
      x=False
    except Exception as B:
     m+=" err:"+str(B)+" type:"+str(type(B))
    finally:
     print(m)
     p.publish(u,m)
     if x:
      reboot_with_reason(p,DDEATH_REASON_OTA)
   elif "\"cmdID\":\"status\"" in m:
    p.publish(O,create_sensor_message())
   elif "\"cmdID\":\"reset\"" in m:
    reboot_with_reason(p,DDEATH_REASON_DCMD_REBOOT)
def connect_and_subscribe():
 global a,l
 p=MQTTClient(a,MQTT_BROKER_ADD)
 p.set_callback(sub_cb)
 m=get_sparkplug_prefx()+",\"ddeath_reasons\": \"-1\"}"
 p.set_last_will(z,m.encode())
 p.connect()
 p.subscribe(l)
 p.publish(n.encode(),create_sensor_message().encode())
 return p
def restart_and_reconnect():
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global M
 global Q
 m=get_sparkplug_prefx()+",\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(M!=""):
  m=m+",\"AnaR\":\""+str(M.read())+"\""
 if(Q!=""):
  m=m+",\"DigR\":\""+str(Q.value())+"\""
 if error!="":
  m=m+",\"err\":\""+error+"\""
 return m+"}"
M=""
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 M=ADC(ANALOG_SENSOR_PIN)
Q=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 Q=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
try:
 p=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
c=0
while True:
 try:
  p.check_msg()
  if(time.time()-c)>MQTT_PUBLISH_INTERVAL:
   p.publish(O,create_sensor_message().encode())
   c=time.time()
 except Exception as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

