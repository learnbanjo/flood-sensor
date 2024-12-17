from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import MQTT_BROKER_ADD,MQTT_PUBLISH_INTERVAL,SPARKPLUGB_GID,SPARKPLUGB_EONID
from HW_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from utils import get_epoch_time
import json
import machine
import time
from umqtt.simple import MQTTClient
P="1.0"
u="spBv1.0/"+SPARKPLUGB_GID
Q=u+"/DCMD"
O=u+"/DDATA/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
U=u+"/DBIRTH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
M=u+"/DDEATH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
z=5
Y=DEVICE_NAME.encode()
r=", \"device_id\": \""+DEVICE_NAME+"\""
J=Q.encode()
L=O.encode()
D=0
def reboot_with_reason(X,reason=0):
 e=get_sparkplug_prefx()+",\"ddeath_reasons\": \""+str(reason)+"\"}"
 X.publish(M.encode(),e.encode)
 X.disconnect()
 time.sleep(5)
 machine.reset() 
def get_sparkplug_prefx():
 global D
 if D>=2147483647:
  D=0
 D+=1
 return "{\"timestamp: \""+str(get_epoch_time())+r+",\"seq\": \""+str(D)+"\""
def sub_cb(topic,msg):
 if topic==J:
  j="\"device_id\":\""+DEVICE_NAME+"\""
  e=msg.decode()
  if(j in e or "\"device_id\":\"*\"" in e):
   if "\"cmdID\":\"OTA\"" in e:
    p=json.loads(e)
    from ota import OTAUpdater
    m="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
    E=p['payload'][0]['otafiles']
    H=True
    e=DEVICE_NAME+" OTA: "+E
    try:
     B=OTAUpdater(m,E)
     if B.check_for_updates():
      if B.download_and_install_update():
       e+=" updated"
      else:
       e+=" update failed"
     else:
      e+=" up-to-date" 
      H=False
    except Exception as T:
     e+=" err:"+str(T)+" type:"+str(type(T))
    finally:
     print(e)
     X.publish(O,e)
     if H:
      reboot_with_reason(X,DDEATH_REASON_OTA)
   elif "\"cmdID\":\"status\"" in e:
    X.publish(L,create_sensor_message())
   elif "\"cmdID\":\"reset\"" in e:
    reboot_with_reason(X,DDEATH_REASON_DCMD_REBOOT)
def connect_and_subscribe():
 global Y,J
 X=MQTTClient(Y,MQTT_BROKER_ADD)
 X.set_callback(sub_cb)
 e=get_sparkplug_prefx()+",\"ddeath_reasons\": \"-1\"}"
 X.set_last_will(M,e.encode())
 X.connect()
 X.subscribe(J)
 q=get_sparkplug_prefx()+"}"
 X.publish(U.encode(),q.encode())
 return X
def restart_and_reconnect():
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global s
 global x
 e=get_sparkplug_prefx()+",\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(s!=""):
  e=e+",\"AnaR\":\""+str(s.read())+"\""
 if(x!=""):
  e=e+",\"DigR\":\""+str(x.value())+"\""
 if error!="":
  e=e+",\"err\":\""+error+"\""
 return e+"}"
s=""
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 s=ADC(ANALOG_SENSOR_PIN)
x=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 x=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
try:
 X=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
v=0
while True:
 try:
  X.check_msg()
  if(time.time()-v)>MQTT_PUBLISH_INTERVAL:
   X.publish(L,create_sensor_message().encode())
   v=time.time()
 except Exception as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

