from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import MQTT_BROKER_ADD,MQTT_PUBLISH_INTERVAL,SPARKPLUGB_GID,SPARKPLUGB_EONID
from HW_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from utils import get_epoch_time
import json
import machine
import time
from umqtt.simple import MQTTClient
t="1.0"
h="spBv1.0/"+SPARKPLUGB_GID
s=h+"/DCMD"
U=h+"/DDATA/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
e=h+"/DBIRTH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
g=h+"/DDEATH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
R=5
B=DEVICE_NAME.encode()
y=", \"device_id\": \""+DEVICE_NAME+"\""
F=s.encode()
P=U.encode()
p=0
def reboot_with_reason(G,reason=0):
 A=get_sparkplug_prefx()+",\"ddeath_reasons\": \""+str(reason)+"\"}"
 G.publish(g.encode(),A.encode)
 G.disconnect()
 time.sleep(5)
 machine.reset() 
def get_sparkplug_prefx():
 global p
 if p>=2147483647:
  p=0
 p+=1
 return "{\"timestamp: \""+str(get_epoch_time())+y+",\"seq\": \""+str(p)+"\""
def sub_cb(topic,msg):
 if topic==F:
  T="\"device_id\":\""+DEVICE_NAME+"\""
  A=msg.decode()
  if(T in A or "\"device_id\":\"*\"" in A):
   if "\"cmdID\":\"OTA\"" in A:
    Q=json.loads(A)
    from ota import OTAUpdater
    E="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
    M=Q['payload'][0]['otafiles']
    q=True
    A=DEVICE_NAME+" OTA: "+M
    try:
     S=OTAUpdater(E,M)
     if S.check_for_updates():
      if S.download_and_install_update():
       A+=" updated"
      else:
       A+=" update failed"
     else:
      A+=" up-to-date" 
      q=False
    except Exception as Y:
     A+=" err:"+str(Y)+" type:"+str(type(Y))
    finally:
     print(A)
     G.publish(U,A)
     if q:
      reboot_with_reason(G,DDEATH_REASON_OTA)
   elif "\"cmdID\":\"status\"" in A:
    G.publish(P,create_sensor_message())
   elif "\"cmdID\":\"reset\"" in A:
    reboot_with_reason(G,DDEATH_REASON_DCMD_REBOOT)
def connect_and_subscribe():
 global B,F
 G=MQTTClient(B,MQTT_BROKER_ADD)
 G.set_callback(sub_cb)
 A=get_sparkplug_prefx()+",\"ddeath_reasons\": \"-1\"}"
 G.set_last_will(g,A.encode())
 G.connect()
 G.subscribe(F)
 O=get_sparkplug_prefx()+"}"
 G.publish(e.encode(),O.encode())
 return G
def restart_and_reconnect():
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global a
 global z
 A=get_sparkplug_prefx()+",\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(a!=""):
  A=A+",\"AnaR\":\""+str(a.read())+"\""
 if(z!=""):
  A=A+",\"DigR\":\""+str(z.value())+"\""
 if error!="":
  A=A+",\"err\":\""+error+"\""
 return A+"}"
a=""
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 a=ADC(ANALOG_SENSOR_PIN)
z=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 z=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
try:
 G=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
j=0
while True:
 try:
  G.check_msg()
  if(time.time()-j)>MQTT_PUBLISH_INTERVAL:
   G.publish(P,create_sensor_message().encode())
   j=time.time()
 except Exception as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

