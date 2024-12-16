from DEVICE_CONFIG import DEVICE_NAME, DEVICE_TYPE, SSID, DEVICE_LOCATION
from DEVICE_CONFIG import ANALOG_SENSOR_PIN, DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address, mqtt_broker_port, mqtt_keep_alive_time, MQTT_PUBLISH_INTERVAL

import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json

VERSION = "1.0"
MQTT_CHECK_INTERVAL = 5

# Define topics
GenericSensorReportTopic = "spBv1.0/flood_sensors"
OTARequestTopic = "spBv1.0/flood_sensors/DCMD"
OTAResponseTopic = "spBv1.0/flood_sensors/DDATA/" + DEVICE_LOCATION + "/" + DEVICE_NAME


if ANALOG_SENSOR_PIN != "":
    from machine import ADC
    analogSensor = ADC(ANALOG_SENSOR_PIN)
else:
    analogSensor = ""

if DIGITAL_SENSOR_PIN != "":
    from machine import Pin
    digitalSensor = Pin(DIGITAL_SENSOR_PIN, Pin.IN, Pin.PULL_UP)
else:
    digitalSensor = ""

mqtt_server = mqtt_broker_address

client_id = ubinascii.hexlify(DEVICE_NAME)
topic_sub = b'spBv1.0/flood_sensors/DCMD'
topic_pub = b'spBv1.0/flood_sensors/DDATA/' + DEVICE_LOCATION + '/' + DEVICE_NAME
print (topic_pub)
last_message = 0
message_interval = MQTT_PUBLISH_INTERVAL

def sub_cb(topic, msg):
  print((topic, msg))
  if topic == b'spBv1.0/flood_sensors/DCMD':
    print('ESP received DCMD message')
    cmdOTAString = "\"name\":\"OTA\""
    cmdStatusString = "\"name\":\"status\""
    # typeString = "\"deviceType\":\"" + DEVICE_TYPE + "\""
    nameString = "\"deviceName\":\"" + DEVICE_NAME + "\""
    allString = "\"deviceName\":\"*\"" 
    message = msg.decode()

    if cmdOTAString in message and (nameString in message or allString in message):
        print('ESP received CMD message: OTA')
        data = json.loads(message)
        from ota import OTAUpdater
        firmware_url = "https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
        otafile = data.get("otafiles")
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
            client.publish(OTAResponseTopic, message)
            time.sleep(5)
            if rebootneeded:
                machine.reset()  # Reset the device to run the new code.
    elif cmdStatusString in message:
        print('ESP received CMD message: status')
        client.publish(topic_pub, create_sensor_message())



def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, mqtt_server)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

def create_sensor_message(error = ""):
    global analogSensor
    global digitalSensor

    message = "{\"devNm\":\"" + DEVICE_NAME + "\",\"devTy\":\"" + DEVICE_TYPE + "\",\"AP\":\"" + SSID + "\""
    if (analogSensor != ""):
        message = message + ",\"AnaR\":\"" + str(analogSensor.read()) + "\""
    if (digitalSensor != ""):
        message = message + ",\"DigR\":\"" + str(digitalSensor.value()) + "\""
    if error != "":
        message = message + ",\"err\":\"" + error + "\""
    return message + "}"

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

while True:
  try:
    client.check_msg()
    if (time.time() - last_message) > message_interval:
      client.publish(topic_pub, create_sensor_message())
      last_message = time.time()
  except OSError as e:
    restart_and_reconnect()
