from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import MQTT_BROKER_ADD,MQTT_PUBLISH_INTERVAL,SPARKPLUGB_GID,SPARKPLUGB_EONID
from HW_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from utils import get_epoch_time
import json
import machine
import time
from umqtt.simple import MQTTClient
y="1.0"
z="spBv1.0/"+SPARKPLUGB_GID
f=z+"/DCMD"
N=z+"/DDATA/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
c=z+"/DBIRTH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
A=z+"/DDEATH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
B=5
g=DEVICE_NAME.encode()
n=", \"device_id\": \""+DEVICE_NAME+"\""
t=f.encode()
h=N.encode()
Y=0
def reboot_with_reason(m,reason=0):
 D=get_sparkplug_prefx()+",\"ddeath_reasons\": \""+str(reason)+"\"}"
 m.publish(A.encode(),D.encode)
 time.sleep(5)
def get_sparkplug_prefx():
 global Y
 if Y>=2147483647:
  Y=0
 Y+=1
 return "{\"timestamp: \""+str(get_epoch_time())+n+",\"seq\": \""+str(Y)+"\""
def sub_cb(topic,msg):
 if topic==t:
  F="\"device_id\":\""+DEVICE_NAME+"\""
  D=msg.decode()
  if(F in D or "\"device_id\":\"*\"" in D):
   if "\"cmdID\":\"OTA\"" in D:
    M=json.loads(D)
    from ota import OTAUpdater
    K="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
    b=M['payload'][0]['otafiles']
    a=True
    D=DEVICE_NAME+" OTA: "+b
    try:
     s=OTAUpdater(K,b)
     if s.check_for_updates():
      if s.download_and_install_update():
       D+=" updated"
      else:
       D+=" update failed"
     else:
      D+=" up-to-date" 
      a=False
    except Exception as o:
     D+=" err:"+str(o)+" type:"+str(type(o))
    finally:
     print(D)
     m.publish(N,D)
     if a:
      reboot_with_reason(m,DDEATH_REASON_OTA)
   elif "\"cmdID\":\"status\"" in D:
    m.publish(h,create_sensor_message())
   elif "\"cmdID\":\"reset\"" in D:
    reboot_with_reason(m,DDEATH_REASON_DCMD_REBOOT)
def connect_and_subscribe():
 global g,t
 m=MQTTClient(g,MQTT_BROKER_ADD)
 m.set_callback(sub_cb)
 D=get_sparkplug_prefx()+",\"ddeath_reasons\": \"-1\"}"
 m.set_last_will(A,D.encode())
 m.connect()
 m.subscribe(t)
 m.publish(c.encode(),create_sensor_message().encode())
 return m
def restart_and_reconnect():
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global e
 global u
 D=get_sparkplug_prefx()+",\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(e!=""):
  D=D+",\"AnaR\":\""+str(e.read())+"\""
 if(u!=""):
  D=D+",\"DigR\":\""+str(u.value())+"\""
 if error!="":
  D=D+",\"err\":\""+error+"\""
 return D+"}"
e=""
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 e=ADC(ANALOG_SENSOR_PIN)
u=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 u=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
try:
 m=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
T=0
while True:
 try:
  m.check_msg()
  if(time.time()-T)>MQTT_PUBLISH_INTERVAL:
   m.publish(h,create_sensor_message().encode())
   T=time.time()
 except Exception as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

