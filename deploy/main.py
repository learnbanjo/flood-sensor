from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import MQTT_BROKER_ADD,MQTT_PUBLISH_INTERVAL,SPARKPLUGB_GID,SPARKPLUGB_EONID
from HW_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from utils import get_epoch_time
import json
import machine
import time
from umqtt.simple import MQTTClient
h="1.0"
H="spBv1.0/"+SPARKPLUGB_GID
E=H+"/DCMD"
O=H+"/DDATA/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
I=H+"/DBIRTH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
T=H+"/DDEATH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
v=5
k=-1 
U=1 
g=2 
M=DEVICE_NAME.encode()
q=", \"device_id\": \""+DEVICE_NAME+"\""
W=E.encode()
r=O.encode()
i=0
def reboot_with_reason(w,reason=0):
 Q=get_sparkplug_prefx()+",\"ddeath_reasons\": \""+str(reason)+"\"}"
 w.publish(T.encode(),Q.encode)
 w.disconnect()
 time.sleep(5)
 machine.reset() 
def get_sparkplug_prefx():
 global i
 if i>=2147483647:
  i=0
 i+=1
 return "{\"timestamp: \""+str(get_epoch_time())+q+",\"seq\": \""+str(i)+"\""
def sub_cb(topic,msg):
 if topic==W:
  X="\"device_id\":\""+DEVICE_NAME+"\""
  Q=msg.decode()
  if(X in Q or "\"device_id\":\"*\"" in Q):
   if "\"cmdID\":\"OTA\"" in Q:
    N=json.loads(Q)
    from ota import OTAUpdater
    j="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
    m=N['payload'][0]['otafiles']
    S=True
    Q=DEVICE_NAME+" OTA: "+m
    try:
     x=OTAUpdater(j,m)
     if x.check_for_updates():
      if x.download_and_install_update():
       Q+=" updated"
      else:
       Q+=" update failed"
     else:
      Q+=" up-to-date" 
      S=False
    except Exception as F:
     Q+=" err:"+str(F)+" type:"+str(type(F))
    finally:
     print(Q)
     w.publish(O,Q)
     if S:
      reboot_with_reason(w,g)
   elif "\"cmdID\":\"status\"" in Q:
    w.publish(r,create_sensor_message())
   elif "\"cmdID\":\"reset\"" in Q:
    reboot_with_reason(w,U)
def connect_and_subscribe():
 global M,W
 w=MQTTClient(M,MQTT_BROKER_ADD)
 w.set_callback(sub_cb)
 Q=get_sparkplug_prefx()+",\"ddeath_reasons\": \"-1\"}"
 w.set_last_will(T,Q.encode())
 w.connect()
 w.subscribe(W)
 P=get_sparkplug_prefx()+"}"
 w.publish(I.encode(),P.encode())
 return w
def restart_and_reconnect():
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global n
 global K
 Q=get_sparkplug_prefx()+",\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(n!=""):
  Q=Q+",\"AnaR\":\""+str(n.read())+"\""
 if(K!=""):
  Q=Q+",\"DigR\":\""+str(K.value())+"\""
 if error!="":
  Q=Q+",\"err\":\""+error+"\""
 return Q+"}"
n=""
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 n=ADC(ANALOG_SENSOR_PIN)
K=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 K=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
try:
 w=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
y=0
while True:
 try:
  w.check_msg()
  if(time.time()-y)>MQTT_PUBLISH_INTERVAL:
   w.publish(r,create_sensor_message().encode())
   y=time.time()
 except Exception as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

