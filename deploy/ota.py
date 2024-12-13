import urequests
import os
import gc
import json
E="1.0"
class OTAUpdater:
 def __init__(T,e,u):
  T.filename=u
  T.repo_url=e
  T.version_file=u+'_'+'ver.json'
  T.version_url=T.process_version_url(e,u) 
  T.firmware_url=e+u 
  if T.version_file in os.listdir():
   with open(T.version_file)as f:
    T.current_version=json.load(f)['version']
  else:
   T.current_version="0"
   with open(T.version_file,'w')as f:
    json.dump({'version':T.current_version},f)
 def process_version_url(T,e,u):
  d=e.replace("raw.githubusercontent.com","github.com") 
  d=d.replace("/","§",4) 
  d=d.replace("/","/latest-commit/",1) 
  d=d.replace("§","/",4) 
  d=d+u 
  return d
 def fetch_latest_code(T)->bool:
  R=urequests.get(T.firmware_url,timeout=20)
  if R.status_code==200:
   gc.collect()
   try:
    T.latest_code=R.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif R.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(T):
  with open('latest_code.py','w')as f:
   f.write(T.latest_code)
  T.current_version=T.latest_version
  with open(T.version_file,'w')as f:
   json.dump({'version':T.current_version},f)
  T.latest_code=None
  os.rename('latest_code.py',T.filename)
 def check_for_updates(T):
  gc.collect()
  A={"accept":"application/json"}
  R=urequests.get(T.version_url,headers=A,timeout=5)
  i=json.loads(R.text)
  T.latest_version=i['oid'] 
  X=True if T.current_version!=T.latest_version else False
  v="New ver: "+str(X)
  print(v) 
  return X
 def download_and_install_update_if_available(T):
  if T.check_for_updates():
   return T.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(T):
  if T.fetch_latest_code():
   T.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

