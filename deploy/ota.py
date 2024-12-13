import urequests
import os
import gc
import json
B="1.0"
class OTAUpdater:
 def __init__(J,Y,v):
  J.filename=v
  J.repo_url=Y
  J.version_file=v+'_'+'ver.json'
  J.version_url=J.process_version_url(Y,v) 
  J.firmware_url=Y+v 
  if J.version_file in os.listdir():
   with open(J.version_file)as f:
    J.current_version=json.load(f)['version']
  else:
   J.current_version="0"
   with open(J.version_file,'w')as f:
    json.dump({'version':J.current_version},f)
 def process_version_url(J,Y,v):
  Q=Y.replace("raw.githubusercontent.com","github.com") 
  Q=Q.replace("/","§",4) 
  Q=Q.replace("/","/latest-commit/",1) 
  Q=Q.replace("§","/",4) 
  Q=Q+v 
  return Q
 def fetch_latest_code(J)->bool:
  b=urequests.get(J.firmware_url,timeout=20)
  if b.status_code==200:
   gc.collect()
   try:
    J.latest_code=b.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif b.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(J):
  with open('latest_code.py','w')as f:
   f.write(J.latest_code)
  J.current_version=J.latest_version
  with open(J.version_file,'w')as f:
   json.dump({'version':J.current_version},f)
  J.latest_code=None
  os.rename('latest_code.py',J.filename)
 def check_for_updates(J):
  gc.collect()
  z={"accept":"application/json"}
  b=urequests.get(J.version_url,headers=z,timeout=5)
  f=json.loads(b.text)
  J.latest_version=f['oid'] 
  K=True if J.current_version!=J.latest_version else False
  w="New ver: "+str(K)
  print(w) 
  return K
 def download_and_install_update_if_available(J):
  if J.check_for_updates():
   return J.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(J):
  if J.fetch_latest_code():
   J.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

