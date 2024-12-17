from DEVICE_CONFIG import DEVICE_NAME, DEVICE_TYPE, SSID
from DEVICE_CONFIG import MQTT_BROKER_ADD, MQTT_PUBLISH_INTERVAL, SPARKPLUGB_GID, SPARKPLUGB_EONID
from HW_CONFIG import ANALOG_SENSOR_PIN, DIGITAL_SENSOR_PIN
from utils import get_epoch_time

import json
import machine
import time
from umqtt.simple import MQTTClient

VERSION = "1.0"

# Define topics
SPARKPLUGB_GP_TOPIC = "spBv1.0/" + SPARKPLUGB_GID
SPARKPLUGB_CMD_TOPIC = SPARKPLUGB_GP_TOPIC + "/DCMD"
SPARKPLUGB_DATA_TOPIC = SPARKPLUGB_GP_TOPIC + "/DDATA/" + SPARKPLUGB_EONID + "/" + DEVICE_NAME
SPARKPLUGB_BIRTHTH_TOPIC = SPARKPLUGB_GP_TOPIC + "/DBIRTH/" + SPARKPLUGB_EONID + "/" + DEVICE_NAME
SPARKPLUGB_DEATH_TOPIC = SPARKPLUGB_GP_TOPIC + "/DDEATH/" + SPARKPLUGB_EONID + "/" + DEVICE_NAME

MQTT_CHECK_INTERVAL = 5
#DDEATH REASON CODE
DDEATH_REASON_UNKNOWN = -1    # -1: unknown. Sent via last will
DDEATH_REASON_DCMD_REBOOT = 1 #  1: DCMD reboot command
DDEATH_REASON_OTA = 2 #  2: OTA reboot

client_id_b = DEVICE_NAME.encode()
device_id_attribute = ", \"device_id\": \"" + DEVICE_NAME + "\""
topic_cmd_b = SPARKPLUGB_CMD_TOPIC.encode()
topic_pub_b = SPARKPLUGB_DATA_TOPIC.encode()
sparkplug_seq = 0
#print (topic_cmd_b)
#print (topic_pub_b)

def reboot_with_reason(client, reason = 0):
    message = get_sparkplug_prefx() + ",\"ddeath_reasons\": \"" + str(reason) + "\"}"
    client.publish(SPARKPLUGB_DEATH_TOPIC.encode(), message.encode)
    client.disconnect()
    time.sleep(5)
    machine.reset()  # Reset the device to run the new code.
       
def get_sparkplug_prefx():
    global sparkplug_seq
    if sparkplug_seq >= 2147483647:
        sparkplug_seq = 0
    sparkplug_seq += 1
    
    return "{\"timestamp: \"" + str(get_epoch_time()) + device_id_attribute + ",\"seq\": \"" + str(sparkplug_seq) + "\""

def sub_cb(topic, msg):
  #print((topic, msg))
  if topic == topic_cmd_b:
    #print('ESP received DCMD message')
    # typeString = "\"deviceType\":\"" + DEVICE_TYPE + "\""
    nameString = "\"device_id\":\"" + DEVICE_NAME + "\""
    message = msg.decode()

    if (nameString in message or "\"device_id\":\"*\"" in message):
      if "\"cmdID\":\"OTA\"" in message:
          #print('ESP received CMD message: OTA')
          data = json.loads(message)
          #print('data:', data)
          from ota import OTAUpdater
          firmware_url = "https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
          otafile = data['payload'][0]['otafiles']
          rebootneeded = True
          message = DEVICE_NAME + " OTA: " + otafile
          try:
              ota_updater = OTAUpdater(firmware_url, otafile)
              if ota_updater.check_for_updates():
                  if ota_updater.download_and_install_update():
                    message += " updated"
                  else:
                    message += " update failed"
              else:
                  message += " up-to-date"        
                  rebootneeded = False
          except Exception as err:
              message += " err:" + str(err) + " type:" + str(type(err))
          
          finally:
              print(message)
              client.publish(SPARKPLUGB_DATA_TOPIC, message)
              if rebootneeded:
                  reboot_with_reason(client, DDEATH_REASON_OTA)
      elif "\"cmdID\":\"status\"" in message:
          #print('ESP received CMD message: status')
          client.publish(topic_pub_b, create_sensor_message())
      elif "\"cmdID\":\"reset\"" in message:
          #print('ESP received CMD message: reboot')
          reboot_with_reason(client, DDEATH_REASON_DCMD_REBOOT)

def connect_and_subscribe():
  global client_id_b, topic_cmd_b
  client = MQTTClient(client_id_b, MQTT_BROKER_ADD)
  client.set_callback(sub_cb)
  message = get_sparkplug_prefx() + ",\"ddeath_reasons\": \"-1\"}"
  client.set_last_will(SPARKPLUGB_DEATH_TOPIC, message.encode())
  client.connect()
  client.subscribe(topic_cmd_b)
  birthmessage = get_sparkplug_prefx() + "}"
  client.publish(SPARKPLUGB_BIRTHTH_TOPIC.encode(), birthmessage.encode())
  #print('Connected to %s MQTT broker, subscribed to %s topic' % (MQTT_BROKER_ADD, topic_cmd_b))
  return client

def restart_and_reconnect():
  #print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

def create_sensor_message(error = ""):
    global analogSensor
    global digitalSensor

    message = get_sparkplug_prefx() + ",\"devNm\":\"" + DEVICE_NAME + "\",\"devTy\":\"" + DEVICE_TYPE + "\",\"AP\":\"" + SSID + "\""
    if (analogSensor != ""):
        message = message + ",\"AnaR\":\"" + str(analogSensor.read()) + "\""
    if (digitalSensor != ""):
        message = message + ",\"DigR\":\"" + str(digitalSensor.value()) + "\""
    if error != "":
        message = message + ",\"err\":\"" + error + "\""
    return message + "}"

# Main program

# Init sensors
analogSensor = ""
if ANALOG_SENSOR_PIN != "":
    from machine import ADC
    analogSensor = ADC(ANALOG_SENSOR_PIN)

digitalSensor = ""
if DIGITAL_SENSOR_PIN != "":
    from machine import Pin
    digitalSensor = Pin(DIGITAL_SENSOR_PIN, Pin.IN, Pin.PULL_UP)

# Connect to MQTT broker and subscribe to command topic
try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

last_message = 0
while True:
  try:
    client.check_msg()
    if (time.time() - last_message) > MQTT_PUBLISH_INTERVAL:
      client.publish(topic_pub_b, create_sensor_message().encode())
      last_message = time.time()
  except Exception as e:
    restart_and_reconnect()
