echo removing main.py_ver.json
sudo ampy -p /dev/tty.usbserial-1410 -b 115200 rm main.py_ver.json
echo done
echo removing ota.py_ver.json
sudo ampy -p /dev/tty.usbserial-1410 -b 115200 put ota.py_ver.json
echo done
echo removing utils.py_ver.json
sudo ampy -p /dev/tty.usbserial-1410 -b 115200 put utils.py_ver.json
echo done
echo removing boot.py_ver.json
sudo ampy -p /dev/tty.usbserial-1410 -b 115200 put boot.py_ver.json
echo done