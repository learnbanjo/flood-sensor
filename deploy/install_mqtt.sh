echo copying DEVICE_CONFIG.py
cp ../DEVICE_CONFIG.py .
sudo ampy -p /dev/tty.usbserial-1410 -b 115200 put DEVICE_CONFIG.py
echo done
echo copying main_mqtt2.py
pyminifier --obfuscate-variables ../main_mqtt2.py > main.py
sudo ampy -p /dev/tty.usbserial-1410 -b 115200 put main.py
echo done
echo copying ota.py
pyminifier --obfuscate-variables ../ota.py > ota.py
sudo ampy -p /dev/tty.usbserial-1410 -b 115200 put ota.py
echo done
echo copying utils.py
pyminifier --obfuscate-variables ../utils.py > utils.py
sudo ampy -p /dev/tty.usbserial-1410 -b 115200 put utils.py
echo done
echo copying boot.py
pyminifier --obfuscate-variables ../boot.py > boot.py
sudo ampy -p /dev/tty.usbserial-1410 -b 115200 put boot.py
echo done
