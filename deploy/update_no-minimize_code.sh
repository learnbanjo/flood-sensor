#this should be run in Python 2 environment
#since pyminifier is not supported in Python 3

echo copying main_mqtt2.py
cp ../src/main_mqtt2.py  main.py
echo done
echo copying ota.py
cp ../src/ota.py ota.py
echo done
echo copying utils.py
cp ../src/utils.py  utils.py
echo done
echo copying boot.py
cp ../src/boot.py  boot.py
echo done
