esptool.py --port /dev/tty.usbserial-1410 erase_flash
esptool.py --port /dev/tty.usbserial-1410 --baud 460800 write_flash --flash_size=detect 0 ESP8266_GENERIC-20241025-v1.24.0.bin

