from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import MQTT_BROKER_ADD,MQTT_PUBLISH_INTERVAL,SPARKPLUGB_GID,SPARKPLUGB_EONID
from HW_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from utils import get_epoch_time
import json
import machine
import time
from umqtt.simple import MQTTClient
l="1.0"
Q="spBv1.0/"+SPARKPLUGB_GID
s=Q+"/DCMD"
f=Q+"/DDATA/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
p=Q+"/DBIRTH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
w=Q+"/DDEATH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
H=5
h=DEVICE_NAME.encode()
j=", \"device_id\": \""+DEVICE_NAME+"\""
k=s.encode()
C=f.encode()
J=0
def reboot_with_reason(G,reason=0):
 D=get_sparkplug_prefx()+",\"ddeath_reasons\": \""+str(reason)+"\"}"
 G.publish(w.encode(),D.encode)
 G.disconnect()
 time.sleep(5)
 machine.reset() 
def get_sparkplug_prefx():
 global J
 if J>=2147483647:
  J=0
 J+=1
 return "{\"timestamp: \""+str(get_epoch_time())+j+",\"seq\": \""+str(J)+"\""
def sub_cb(topic,msg):
 if topic==k:
  E="\"device_id\":\""+DEVICE_NAME+"\""
  D=msg.decode()
  if(E in D or "\"device_id\":\"*\"" in D):
   if "\"cmdID\":\"OTA\"" in D:
    g=json.loads(D)
    from ota import OTAUpdater
    t="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
    X=g['payload'][0]['otafiles']
    S=True
    D=DEVICE_NAME+" OTA: "+X
    try:
     P=OTAUpdater(t,X)
     if P.check_for_updates():
      if P.download_and_install_update():
       D+=" updated"
      else:
       D+=" update failed"
     else:
      D+=" up-to-date" 
      S=False
    except Exception as I:
     D+=" err:"+str(I)+" type:"+str(type(I))
    finally:
     print(D)
     G.publish(f,D)
     if S:
      reboot_with_reason(G,DDEATH_REASON_OTA)
   elif "\"cmdID\":\"status\"" in D:
    G.publish(C,create_sensor_message())
   elif "\"cmdID\":\"reset\"" in D:
    reboot_with_reason(G,DDEATH_REASON_DCMD_REBOOT)
def connect_and_subscribe():
 global h,k
 G=MQTTClient(h,MQTT_BROKER_ADD)
 G.set_callback(sub_cb)
 D=get_sparkplug_prefx()+",\"ddeath_reasons\": \"-1\"}"
 G.set_last_will(w,D.encode())
 G.connect()
 G.subscribe(k)
 O=get_sparkplug_prefx()+"}"
 G.publish(p.encode(),O.encode())
 return G
def restart_and_reconnect():
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global i
 global z
 D=get_sparkplug_prefx()+",\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(i!=""):
  D=D+",\"AnaR\":\""+str(i.read())+"\""
 if(z!=""):
  D=D+",\"DigR\":\""+str(z.value())+"\""
 if error!="":
  D=D+",\"err\":\""+error+"\""
 return D+"}"
i=""
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 i=ADC(ANALOG_SENSOR_PIN)
z=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 z=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
try:
 G=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
c=0
while True:
 try:
  G.check_msg()
  if(time.time()-c)>MQTT_PUBLISH_INTERVAL:
   G.publish(C,create_sensor_message().encode())
   c=time.time()
 except Exception as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

