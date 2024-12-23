import urequests
import os
import gc
import json
C="1.0"
class OTAUpdater:
 def __init__(L,K,v):
  L.filename=v
  L.repo_url=K
  L.version_file=v+'_'+'ver.json'
  L.version_url=L.process_version_url(K,v) 
  L.firmware_url=K+v 
  print("Version URL is ",L.version_url)
  print("Firmware URL is ",L.firmware_url)
  if L.version_file in os.listdir():
   with open(L.version_file)as f:
    L.current_version=json.load(f)['version']
   j="Current "+L.filename+" is "+L.current_version
   print("version message ",j)
  else:
   print("No version file")
   L.current_version="0"
   with open(L.version_file,'w')as f:
    json.dump({'version':L.current_version},f)
 def process_version_url(L,K,v):
  H=K.replace("raw.githubusercontent.com","github.com") 
  H=H.replace("/","§",4) 
  H=H.replace("/","/latest-commit/",1) 
  H=H.replace("§","/",4) 
  H=H+v 
  return H
 def fetch_latest_code(L)->bool:
  O=urequests.get(L.firmware_url,timeout=20)
  if O.status_code==200:
   gc.collect()
   try:
    L.latest_code=O.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif O.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(L):
  with open('latest_code.py','w')as f:
   f.write(L.latest_code)
  L.current_version=L.latest_version
  with open(L.version_file,'w')as f:
   json.dump({'version':L.current_version},f)
  L.latest_code=None
  os.rename('latest_code.py',L.filename)
 def check_for_updates(L):
  print('Checking for latest version...')
  gc.collect()
  Q={"accept":"application/json"}
  O=urequests.get(L.version_url,headers=Q,timeout=5)
  A=json.loads(O.text)
  L.latest_version=A['oid'] 
  B=True if L.current_version!=L.latest_version else False
  y="New ver: "+str(B)
  print(y) 
  return B
 def download_and_install_update_if_available(L):
  if L.check_for_updates():
   return L.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(L):
  if L.fetch_latest_code():
   L.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

