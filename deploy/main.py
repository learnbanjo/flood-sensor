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
c="1.0"
h="spBv1.0/"+SPARKPLUGB_GID
P=h+"/DCMD"
m=h+"/DDATA/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
r=h+"/DBIRTH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
w=h+"/DDEATH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
Y=5
B=DEVICE_NAME.encode()
l=", \"device_id\": \""+DEVICE_NAME+"\""
O=P.encode()
F=m.encode()
C=0
def reboot_with_reason(t,reason=0):
 j=get_sparkplug_prefx()+",\"ddeath_reasons\": \""+str(reason)+"\"}"
 t.publish(w.encode(),j.encode)
 t.disconnect()
 time.sleep(5)
 machine.reset() 
def get_sparkplug_prefx():
 global C
 C+=1
 return "{\"timestamp: \""+str(get_epoch_time())+l+",\"seq\": \""+str(C)+"\""
def sub_cb(topic,msg):
 if topic==O:
  E="\"device_id\":\""+DEVICE_NAME+"\""
  j=msg.decode()
  if(E in j or "\"device_id\":\"*\"" in j):
   if "\"cmdID\":\"OTA\"" in j:
    f=json.loads(j)
    from ota import OTAUpdater
    T="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
    M=f['payload'][0]['otafiles']
    G=True
    j=DEVICE_NAME+" OTA: "+M
    try:
     W=OTAUpdater(T,M)
     if W.check_for_updates():
      if W.download_and_install_update():
       j+=" updated"
      else:
       j+=" update failed"
     else:
      j+=" up-to-date" 
      G=False
    except Exception as i:
     j+=" err:"+str(i)+" type:"+str(type(i))
    finally:
     print(j)
     t.publish(m,j)
     if G:
      reboot_with_reason(t,DDEATH_REASON_OTA)
   elif "\"cmdID\":\"status\"" in j:
    t.publish(F,create_sensor_message())
   elif "\"cmdID\":\"reset\"" in j:
    reboot_with_reason(t,DDEATH_REASON_DCMD_REBOOT)
def connect_and_subscribe():
 global B,O
 t=MQTTClient(B,MQTT_BROKER_ADD)
 t.set_callback(sub_cb)
 j=get_sparkplug_prefx()+",\"ddeath_reasons\": \"-1\"}"
 t.set_last_will(w,j.encode())
 t.connect()
 t.subscribe(O)
 v=get_sparkplug_prefx()+"}"
 t.publish(r.encode(),v.encode())
 return t
def restart_and_reconnect():
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global X
 global I
 j=get_sparkplug_prefx()+",\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(X!=""):
  j=j+",\"AnaR\":\""+str(X.read())+"\""
 if(I!=""):
  j=j+",\"DigR\":\""+str(I.value())+"\""
 if error!="":
  j=j+",\"err\":\""+error+"\""
 return j+"}"
X=""
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 X=ADC(ANALOG_SENSOR_PIN)
I=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 I=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
try:
 t=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
U=0
while True:
 try:
  t.check_msg()
  if(time.time()-U)>MQTT_PUBLISH_INTERVAL:
   t.publish(F,create_sensor_message().encode())
   U=time.time()
 except Exception as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

