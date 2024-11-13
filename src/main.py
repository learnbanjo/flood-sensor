import machine
import time

try:
    from DEVICE_CONFIG import DEVICE_NAME, DEVICE_TYPE, SSID, PASSWORD
    from DEVICE_CONFIG import ANALOG_SENSOR_PIN, DIGITAL_SENSOR_PIN

    # DEVICE_NAME default depends on the device
    # SSID default depends on the device
    # PASSWORD default is none ""
    # OTA_ENABLED default is "false"

    if ANALOG_SENSOR_PIN != "":
        from machine import ADC
        analogSensor = ADC(ANALOG_SENSOR_PIN)
    else:
        analogSensor = ""

    if DIGITAL_SENSOR_PIN != "":
        from machine import Pin
        digigalSensor = Pin(DIGITAL_SENSOR_PIN, Pin.IN, Pin.PULL_UP)
    else:
        digigalSensor = ""

    import socket
    import utils

    URLKEY_OTA = "ota"
    VERSION = "1.0"

    analogSensor_value = ""
    digitalSensor_value = ""
    URLParameters = {}

    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    while True:
        cl, addr = s.accept()
        print("client connected from", addr)

        cl_file = cl.makefile("rwb", 0)
        URLParameters = {}
        while True:
            line = cl_file.readline()
            if not line or line == b"\r\n":
                break
            else:
                HTTPOptions = line.split()
                if len(HTTPOptions) > 2:
                    if (HTTPOptions[0] == b"GET"):
                        URLOptions = str(HTTPOptions[1].decode()).split('?')
                        if len(URLOptions) >= 2:
                            URLParameters = utils.qs_parse(URLOptions[1])

        if (analogSensor != ""):
            analogSensor_value = analogSensor.read()
        if (digigalSensor != ""):
            digitalSensor_value = digigalSensor.value()

        cl.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
        message = "{"
        message = message + "\"deviceName\":\"" + DEVICE_NAME + "\""
        message = message + ",\"deviceType\":\"" + DEVICE_TYPE + "\""
        message = message + ",\"AP\":\"" + SSID + "\""
        if ANALOG_SENSOR_PIN != "":
            message = message + ",\"analogSensorReading\":\"" + str(analogSensor_value) + "\""
        if DIGITAL_SENSOR_PIN != "":
            message = message + ",\"digitalSensorReading\":\"" + str(digitalSensor_value) + "\""
        message = message + "}"
        cl.send(message)

        if (URLParameters.get(URLKEY_OTA, "False") == "True"):
            from ota import OTAUpdater
            firmware_url = "https://raw.githubusercontent.com/learnbanjo/flood-sensor/main/src/"
            try:
                ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "ota.py")
                ota_updater.download_and_install_update_if_available()
                ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "main.py")
                ota_updater.download_and_install_update_if_available()
                ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "boot.py")
                ota_updater.download_and_install_update_if_available()
                ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "utils.py")
                ota_updater.download_and_install_update_if_available()
                cl.send('<p>OTA completed. Rebooting...')
            except Exception as err:
                print("OTA failed.")
                print("Unexpected error:", err, " type:", type(err))
                cl.send('<p>OTA failed.')
                cl.send("Unexpected errorr=", err, " type=", type(err))
            cl.close()
            time.sleep(5)
            machine.reset()  # Reset the device to run the new code.
        cl.close()
except KeyboardInterrupt:
    raise
except Exception as err:
    cl.close()
    print("Unexpected error:", err, " type:", type(err))
    machine.reset() 