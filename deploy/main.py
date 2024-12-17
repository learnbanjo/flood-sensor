from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import MQTT_BROKER_ADD,MQTT_PUBLISH_INTERVAL,SPARKPLUGB_GID,SPARKPLUGB_EONID
from HW_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from utils import get_epoch_time
import json
import machine
import time
from umqtt.simple import MQTTClient
G="1.0"
J="spBv1.0/"+SPARKPLUGB_GID
z=J+"/DCMD"
P=J+"/DDATA/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
k=J+"/DBIRTH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
T=J+"/DDEATH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
i=5
f=-1 
S=1 
V=2 
b=DEVICE_NAME.encode()
t=", \"device_id\": \""+DEVICE_NAME+"\""
e=z.encode()
R=P.encode()
A=0
def reboot_with_reason(I,reason=0):
 X=get_sparkplug_prefx()+",\"ddeath_reasons\": \""+str(reason)+"\"}"
 I.publish(T.encode(),X.encode)
 I.disconnect()
 time.sleep(5)
 machine.reset() 
def get_sparkplug_prefx():
 global A
 if A>=2147483647:
  A=0
 A+=1
 return "{\"timestamp: \""+str(get_epoch_time())+t+",\"seq\": \""+str(A)+"\""
def sub_cb(topic,msg):
 if topic==e:
  C="\"device_id\":\""+DEVICE_NAME+"\""
  X=msg.decode()
  if(C in X or "\"device_id\":\"*\"" in X):
   if "\"cmdID\":\"OTA\"" in X:
    w=json.loads(X)
    from ota import OTAUpdater
    x="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
    s=w['payload'][0]['otafiles']
    D=True
    X=DEVICE_NAME+" OTA: "+s
    try:
     Y=OTAUpdater(x,s)
     if Y.check_for_updates():
      if Y.download_and_install_update():
       X+=" updated"
      else:
       X+=" update failed"
     else:
      X+=" up-to-date" 
      D=False
    except Exception as N:
     X+=" err:"+str(N)+" type:"+str(type(N))
    finally:
     print(X)
     I.publish(P,X)
     if D:
      reboot_with_reason(I,V)
   elif "\"cmdID\":\"status\"" in X:
    I.publish(R,create_sensor_message())
   elif "\"cmdID\":\"reset\"" in X:
    reboot_with_reason(I,S)
def connect_and_subscribe():
 global b,e
 I=MQTTClient(b,MQTT_BROKER_ADD)
 I.set_callback(sub_cb)
 X=get_sparkplug_prefx()+",\"ddeath_reasons\": \"-1\"}"
 I.set_last_will(T,X.encode())
 I.connect()
 I.subscribe(e)
 M=get_sparkplug_prefx()+"}"
 I.publish(k.encode(),M.encode())
 return I
def restart_and_reconnect():
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global Q
 global B
 X=get_sparkplug_prefx()+",\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(Q!=""):
  X=X+",\"AnaR\":\""+str(Q.read())+"\""
 if(B!=""):
  X=X+",\"DigR\":\""+str(B.value())+"\""
 if error!="":
  X=X+",\"err\":\""+error+"\""
 return X+"}"
Q=""
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 Q=ADC(ANALOG_SENSOR_PIN)
B=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 B=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
try:
 I=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
E=0
while True:
 try:
  I.check_msg()
  if(time.time()-E)>MQTT_PUBLISH_INTERVAL:
   I.publish(R,create_sensor_message().encode())
   E=time.time()
 except Exception as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

