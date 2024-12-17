
from DEVICE_CONFIG import DEVICE_NAME, DEVICE_TYPE, SSID, PASSWORD
from DEVICE_CONFIG import SPARKPLUGB_EONID, SPARKPLUGB_GID
from DEVICE_CONFIG import MQTT_BROKER_ADD, MQTT_BROKER_PORT, MQTT_KEEP_ALIVE_TIME, MQTT_PUBLISH_INTERVAL
#import machine
import time
from umqtt.simple import MQTTClient

VERSION = "1.0"
MQTT_CHECK_INTERVAL = 5

# Define topics
GenericSensorReportTopic = "spBv1.0/flood_sensor/DDATA/#"
OTARequestTopic = "spBv1.0/flood_sensor/DCMD"
#OTAResponseTopic = "spBv1.0/flood_sensor/DDATA"

def getMqttClient():
    try:
        client = MQTTClient("TEST_MQTT".encode(), server = MQTT_BROKER_ADD, port = MQTT_BROKER_PORT, keepalive = MQTT_KEEP_ALIVE_TIME)
        client.set_callback(on_mqtt_callback)
        client.connect()
        client.subscribe(GenericSensorReportTopic)
        return client
    except Exception as str_error:
        print(f"GenericSensor: Create MQTT client with exception: {str(str_error)}")
        if client != None:
            client.disconnect()
        return None

def on_mqtt_callback(client, userdata, msg):
    print(f"on_mqtt_callback: {msg.topic} {msg.payload}")

def create_ota_message(deviceName = DEVICE_NAME, deviceType = DEVICE_TYPE, otafiles = "utils.py", cmdID = "status"):
    device_id_attribute = ", \"device_id\": \"test-host\""
    message = "{"
    message = message + "\"timestamp: \"" + str(int(time.time())) + device_id_attribute
    message = message + ", \"payload\": [{"
    message = message + "\"cmdID\":\"" + cmdID + "\""
    message = message + ",\"device_id\":\"" + deviceName + "\""
    message = message + ",\"device_type\":\"" + deviceType + "\""
    if (cmdID == "OTA"):
        message = message + ",\"otafiles\":\"" + otafiles + "\""
    message = message + "}]"
    message = message + "}"
    return message

client = None
while client == None:
    client = getMqttClient()
    if client == None:
        time.sleep(10)
try:

    time_since_last_publish = MQTT_PUBLISH_INTERVAL
    otafiles = ["utils.py", "ota.py", "main.py", "boot.py"]
    cmds = ["status", "OTA", "reset"]
    otafiles_index = 0
    cmds_index = 0

    while True:
        if time_since_last_publish >= MQTT_PUBLISH_INTERVAL:
            message = create_ota_message(deviceName=DEVICE_NAME, deviceType=DEVICE_TYPE, otafiles=otafiles[otafiles_index], cmdID = cmds[cmds_index])
            client.publish(OTARequestTopic, message.encode(), qos=1)
            time_since_last_publish = 0
            print(f"Published: {message}")
            otafiles_index += 1
            cmds_index += 1
            otafiles_index = otafiles_index % len(otafiles)
            cmds_index = cmds_index % len(cmds)
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
