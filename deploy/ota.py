import urequests
import os
import gc
import json
l="1.0"
class OTAUpdater:
 def __init__(K,L,u):
  K.filename=u
  K.repo_url=L
  K.version_file=u+'_'+'ver.json'
  K.version_url=K.process_version_url(L,u) 
  K.firmware_url=L+u 
  if K.version_file in os.listdir():
   with open(K.version_file)as f:
    K.current_version=json.load(f)['version']
  else:
   K.current_version="0"
   with open(K.version_file,'w')as f:
    json.dump({'version':K.current_version},f)
 def process_version_url(K,L,u):
  X=L.replace("raw.githubusercontent.com","github.com") 
  X=X.replace("/","§",4) 
  X=X.replace("/","/latest-commit/",1) 
  X=X.replace("§","/",4) 
  X=X+u 
  return X
 def fetch_latest_code(K)->bool:
  d=urequests.get(K.firmware_url,timeout=20)
  if d.status_code==200:
   gc.collect()
   try:
    K.latest_code=d.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif d.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(K):
  with open('latest_code.py','w')as f:
   f.write(K.latest_code)
  K.current_version=K.latest_version
  with open(K.version_file,'w')as f:
   json.dump({'version':K.current_version},f)
  K.latest_code=None
  os.rename('latest_code.py',K.filename)
 def check_for_updates(K):
  gc.collect()
  o={"accept":"application/json"}
  d=urequests.get(K.version_url,headers=o,timeout=5)
  I=json.loads(d.text)
  K.latest_version=I['oid'] 
  x=True if K.current_version!=K.latest_version else False
  S="New ver: "+str(x)
  print(S) 
  return x
 def download_and_install_update_if_available(K):
  if K.check_for_updates():
   return K.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(K):
  if K.fetch_latest_code():
   K.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

