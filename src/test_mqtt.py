
from DEVICE_CONFIG import DEVICE_NAME, DEVICE_TYPE, SSID, PASSWORD
from DEVICE_CONFIG import ANALOG_SENSOR_PIN, DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address, mqtt_broker_port, mqtt_keep_alive_time, MQTT_PUBLISH_INTERVAL
import machine
import time
from umqtt.simple import MQTTClient

VERSION = "1.0"
MQTT_CHECK_INTERVAL = 5

# Define topics
GenericSensorReportTopic = "GenericSensor/SensorData"
OTARequestTopic = "OTA/OTARequest"
OTAResponseTopic = "OTA/OTAResponse"

def getMqttClient():
    try:
        client = MQTTClient("TEST_MQTT".encode(), server = mqtt_broker_address, port = mqtt_broker_port, keepalive = mqtt_keep_alive_time)
        client.set_callback(on_mqtt_callback)
        client.connect()
        client.subscribe(GenericSensorReportTopic)
        client.subscribe(OTAResponseTopic)
        return client
    except Exception as str_error:
        print(f"GenericSensor: Create MQTT client with exception: {str(str_error)}")
        if client != None:
            client.disconnect()
        return None

def on_mqtt_callback(client, userdata, msg):
    print(f"on_mqtt_callback: {msg.topic} {msg.payload}")

def create_ota_message(deviceName = DEVICE_NAME, deviceType = DEVICE_TYPE, otafiles = "utils.py"):
    message = "{"
    message = message + "\"deviceName\":\"" + deviceName + "\""
    message = message + ",\"deviceType\":\"" + deviceType + "\""
    message = message + ",\"otafiles\":\"" + otafiles + "\""
    message = message + "}"
    return message

client = None
while client == None:
    client = getMqttClient()
    if client == None:
        time.sleep(10)
try:

 #   time_since_last_publish = 0
    time_since_last_publish = MQTT_PUBLISH_INTERVAL
    otafiles = ["utils.py", "ota.py", "main.py", "boot.py"]
    otafiles_index = 0

    while True:
        if time_since_last_publish >= MQTT_PUBLISH_INTERVAL:
            message = create_ota_message(deviceName=DEVICE_NAME, deviceType=DEVICE_TYPE, otafiles=otafiles[otafiles_index])
            client.publish(OTARequestTopic, message.encode(), qos=1)
            time_since_last_publish = 0
            print(f"Published: {message}")
            otafiles_index += 1
            otafiles_index = otafiles_index % len(otafiles)
        else:
            time_since_last_publish += MQTT_CHECK_INTERVAL

        client.check_msg()
        time.sleep(MQTT_CHECK_INTERVAL)


except KeyboardInterrupt:
    client.disconnect()
    print("KeyboardInterrupt")
    raise
except Exception as err:
    print("Unexpected error:", err, " type:", type(err))
    message = "Unexpected error:" + str(err) + " type:" + str(type(err))
    client.publish(GenericSensorReportTopic, message )
    client.disconnect()
    machine.reset() 
