DEVICE_NAME = "device host name" # Descriptive name for the device
DEVICE_TYPE = "Flood Sensor" # Sensor Type. "Flood Sensor", "Pressure Sensor"
DEVICE_KEY = "" #device private key for future use cases
SSID = "my wifi hotspot name"
PASSWORD = "wifi password" #Use "" for no password
ANALOG_SENSOR_PIN = 0 # ESP8266 ADC pin is 0. Set to "" to disable
DIGITAL_SENSOR_PIN = 5 # ESP8266 GPIO pin is D1 (GPIO5). Set to "" to disable. See https://electropeak.com/learn/esp8266-pinout-reference-how-to-use-esp8266-gpio-pins/

MQTT_PUBLISH_INTERVAL = 30
mqtt_broker_address = "127.0.0.1"
mqtt_broker_port = 1883
mqtt_keep_alive_time = 360
