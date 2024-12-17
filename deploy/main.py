from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import MQTT_BROKER_ADD,MQTT_PUBLISH_INTERVAL,SPARKPLUGB_GID,SPARKPLUGB_EONID
from HW_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from utils import get_epoch_time
import json
import machine
import time
from umqtt.simple import MQTTClient
K="1.0"
s="spBv1.0/"+SPARKPLUGB_GID
z=s+"/DCMD"
l=s+"/DDATA/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
m=s+"/DBIRTH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
c=s+"/DDEATH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
q=5
W=DEVICE_NAME.encode()
k=", \"device_id\": \""+DEVICE_NAME+"\""
Q=z.encode()
x=l.encode()
t=0
def reboot_with_reason(b,reason=0):
 e=get_sparkplug_prefx()+",\"ddeath_reasons\": \""+str(reason)+"\"}"
 b.publish(c.encode(),e.encode)
 time.sleep(5)
def get_sparkplug_prefx():
 global t
 if t>=2147483647:
  t=0
 t+=1
 return "{\"timestamp: \""+str(get_epoch_time())+k+",\"seq\": \""+str(t)+"\""
def sub_cb(topic,msg):
 if topic==Q:
  n="\"device_id\":\""+DEVICE_NAME+"\""
  e=msg.decode()
  if(n in e or "\"device_id\":\"*\"" in e):
   if "\"cmdID\":\"OTA\"" in e:
    g=json.loads(e)
    from ota import OTAUpdater
    a="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
    j=g['payload'][0]['otafiles']
    r=True
    e=DEVICE_NAME+" OTA: "+j
    try:
     T=OTAUpdater(a,j)
     if T.check_for_updates():
      if T.download_and_install_update():
       e+=" updated"
      else:
       e+=" update failed"
     else:
      e+=" up-to-date" 
      r=False
    except Exception as G:
     e+=" err:"+str(G)+" type:"+str(type(G))
    finally:
     print(e)
     b.publish(l,e)
     if r:
      reboot_with_reason(b,DDEATH_REASON_OTA)
   elif "\"cmdID\":\"status\"" in e:
    b.publish(x,create_sensor_message())
   elif "\"cmdID\":\"reset\"" in e:
    reboot_with_reason(b,DDEATH_REASON_DCMD_REBOOT)
def connect_and_subscribe():
 global W,Q
 b=MQTTClient(W,MQTT_BROKER_ADD)
 b.set_callback(sub_cb)
 e=get_sparkplug_prefx()+",\"ddeath_reasons\": \"-1\"}"
 b.set_last_will(c,e.encode())
 b.connect()
 b.subscribe(Q)
 b.publish(m.encode(),create_sensor_message().encode())
 return b
def restart_and_reconnect():
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global N
 global h
 e=get_sparkplug_prefx()+",\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(N!=""):
  e=e+",\"AnaR\":\""+str(N.read())+"\""
 if(h!=""):
  e=e+",\"DigR\":\""+str(h.value())+"\""
 if error!="":
  e=e+",\"err\":\""+error+"\""
 return e+"}"
N=""
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 N=ADC(ANALOG_SENSOR_PIN)
h=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 h=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
try:
 b=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
u=0
while True:
 try:
  b.check_msg()
  if(time.time()-u)>MQTT_PUBLISH_INTERVAL:
   b.publish(x,create_sensor_message().encode())
   u=time.time()
 except Exception as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

