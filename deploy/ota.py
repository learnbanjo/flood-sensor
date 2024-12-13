import urequests
import os
import gc
import json
m="1.0"
class OTAUpdater:
 def __init__(j,k,L):
  j.filename=L
  j.repo_url=k
  j.version_file=L+'_'+'ver.json'
  j.version_url=j.process_version_url(k,L) 
  j.firmware_url=k+L 
  if j.version_file in os.listdir():
   with open(j.version_file)as f:
    j.current_version=json.load(f)['version']
  else:
   j.current_version="0"
   with open(j.version_file,'w')as f:
    json.dump({'version':j.current_version},f)
 def process_version_url(j,k,L):
  D=k.replace("raw.githubusercontent.com","github.com") 
  D=D.replace("/","§",4) 
  D=D.replace("/","/latest-commit/",1) 
  D=D.replace("§","/",4) 
  D=D+L 
  return D
 def fetch_latest_code(j)->bool:
  Q=urequests.get(j.firmware_url,timeout=20)
  if Q.status_code==200:
   gc.collect()
   try:
    j.latest_code=Q.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif Q.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(j):
  with open('latest_code.py','w')as f:
   f.write(j.latest_code)
  j.current_version=j.latest_version
  with open(j.version_file,'w')as f:
   json.dump({'version':j.current_version},f)
  j.latest_code=None
  os.rename('latest_code.py',j.filename)
 def check_for_updates(j):
  gc.collect()
  d={"accept":"application/json"}
  Q=urequests.get(j.version_url,headers=d,timeout=5)
  i=json.loads(Q.text)
  j.latest_version=i['oid'] 
  A=True if j.current_version!=j.latest_version else False
  Y="New ver: "+str(A)
  print(Y) 
  return A
 def download_and_install_update_if_available(j):
  if j.check_for_updates():
   return j.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(j):
  if j.fetch_latest_code():
   j.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

