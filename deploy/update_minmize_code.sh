#this should be run in Python 2 environment
#since pyminifier is not supported in Python 3

echo copying main_mqtt2.py
pyminifier --obfuscate-variables ../src/main_mqtt2.py > main.py
echo done
echo copying ota.py
pyminifier --obfuscate-variables ../src/ota.py > ota.py
echo done
echo copying utils.py
pyminifier --obfuscate-variables ../src/utils.py > utils.py
echo done
echo copying boot.py
pyminifier --obfuscate-variables ../src/boot.py > boot.py
echo done
