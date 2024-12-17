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
b="1.0"
k="spBv1.0/"+SPARKPLUGB_GID
S=k+"/DCMD"
L=k+"/DDATA/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
P=k+"/DBIRTH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
A=k+"/DDEATH/"+SPARKPLUGB_EONID+"/"+DEVICE_NAME
T=5
j=DEVICE_NAME.encode()
M=", \"device_id\": \""+DEVICE_NAME+"\""
q=S.encode()
u=L.encode()
i=0
def reboot_with_reason(R,reason=0):
 K=get_sparkplug_prefx()+",\"ddeath_reasons\": \""+str(reason)+"\"}"
 R.publish(A.encode(),K.encode)
 R.disconnect()
 time.sleep(5)
 machine.reset() 
def get_sparkplug_prefx():
 global i
 if i>=2147483647:
  i=0
 i+=1
 return "{\"timestamp: \""+str(get_epoch_time())+M+",\"seq\": \""+str(i)+"\""
def sub_cb(topic,msg):
 if topic==q:
  W="\"device_id\":\""+DEVICE_NAME+"\""
  K=msg.decode()
  if(W in K or "\"device_id\":\"*\"" in K):
   if "\"cmdID\":\"OTA\"" in K:
    G=json.loads(K)
    from ota import OTAUpdater
    v="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
    z=G['payload'][0]['otafiles']
    O=True
    K=DEVICE_NAME+" OTA: "+z
    try:
     t=OTAUpdater(v,z)
     if t.check_for_updates():
      if t.download_and_install_update():
       K+=" updated"
      else:
       K+=" update failed"
     else:
      K+=" up-to-date" 
      O=False
    except Exception as n:
     K+=" err:"+str(n)+" type:"+str(type(n))
    finally:
     print(K)
     R.publish(L,K)
     if O:
      reboot_with_reason(R,DDEATH_REASON_OTA)
   elif "\"cmdID\":\"status\"" in K:
    R.publish(u,create_sensor_message())
   elif "\"cmdID\":\"reset\"" in K:
    reboot_with_reason(R,DDEATH_REASON_DCMD_REBOOT)
def connect_and_subscribe():
 global j,q
 R=MQTTClient(j,MQTT_BROKER_ADD)
 R.set_callback(sub_cb)
 K=get_sparkplug_prefx()+",\"ddeath_reasons\": \"-1\"}"
 R.set_last_will(A,K.encode())
 R.connect()
 R.subscribe(q)
 g=get_sparkplug_prefx()+"}"
 R.publish(P.encode(),g.encode())
 return R
def restart_and_reconnect():
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global s
 global e
 K=get_sparkplug_prefx()+",\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(s!=""):
  K=K+",\"AnaR\":\""+str(s.read())+"\""
 if(e!=""):
  K=K+",\"DigR\":\""+str(e.value())+"\""
 if error!="":
  K=K+",\"err\":\""+error+"\""
 return K+"}"
s=""
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 s=ADC(ANALOG_SENSOR_PIN)
e=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 e=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
try:
 R=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
J=0
while True:
 try:
  R.check_msg()
  if(time.time()-J)>MQTT_PUBLISH_INTERVAL:
   R.publish(u,create_sensor_message().encode())
   J=time.time()
 except Exception as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

