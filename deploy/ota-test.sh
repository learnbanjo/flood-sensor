#scipt for ota testing
#this should be run in Python 2 environment

counter=0

while [ $counter -lt 100 ]
do
    echo "OTA Test Counter: $counter"
    ((counter++))
    source update_minmize_code.sh
    ls -al *.py
    git add boot.py main.py ota.py utils.py 
    git commit -m "ota test $counter, re-minimize only, no code change"
    git push origin deploy-test
    sleep 300
done