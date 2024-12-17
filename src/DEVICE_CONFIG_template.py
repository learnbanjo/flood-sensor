DEVICE_NAME = "FS_bh_basement" # Descriptive name for the device
DEVICE_TYPE = "flood_sensor" # Sensor Type. "Flood Sensor", "Pressure Sensor"
DEVICE_KEY = "" #device private key for future use cases
SPARKPLUGB_GID = "flood_sensor"  # Sparkplug B Group ID, usually is device type
SPARKPLUGB_EONID = "bh" # Sparkplug B Edge of Network ID, usually is building name
SSID = "my wifi hotspot name"
PASSWORD = "wifi password" #Use "" for no password

MQTT_PUBLISH_INTERVAL = 300
MQTT_BROKER_ADD = "127.0.0.1"
MQTT_BROKER_PORT = 1883
MQTT_KEEP_ALIVE_TIME = 360
