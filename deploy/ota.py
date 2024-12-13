import urequests
import os
import gc
import json
P="1.0"
class OTAUpdater:
 def __init__(K,m,j):
  K.filename=j
  K.repo_url=m
  K.version_file=j+'_'+'ver.json'
  K.version_url=K.process_version_url(m,j) 
  K.firmware_url=m+j 
  if K.version_file in os.listdir():
   with open(K.version_file)as f:
    K.current_version=json.load(f)['version']
  else:
   K.current_version="0"
   with open(K.version_file,'w')as f:
    json.dump({'version':K.current_version},f)
 def process_version_url(K,m,j):
  C=m.replace("raw.githubusercontent.com","github.com") 
  C=C.replace("/","§",4) 
  C=C.replace("/","/latest-commit/",1) 
  C=C.replace("§","/",4) 
  C=C+j 
  return C
 def fetch_latest_code(K)->bool:
  R=urequests.get(K.firmware_url,timeout=20)
  if R.status_code==200:
   gc.collect()
   try:
    K.latest_code=R.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif R.status_code==404:
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
  U={"accept":"application/json"}
  R=urequests.get(K.version_url,headers=U,timeout=5)
  n=json.loads(R.text)
  K.latest_version=n['oid'] 
  X=True if K.current_version!=K.latest_version else False
  A="New ver: "+str(X)
  print(A) 
  return X
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

