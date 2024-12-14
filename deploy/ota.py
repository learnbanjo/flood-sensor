import urequests
import os
import gc
import json
H="1.0"
class OTAUpdater:
 def __init__(F,D,K):
  F.filename=K
  F.repo_url=D
  F.version_file=K+'_'+'ver.json'
  F.version_url=F.process_version_url(D,K) 
  F.firmware_url=D+K 
  if F.version_file in os.listdir():
   with open(F.version_file)as f:
    F.current_version=json.load(f)['version']
  else:
   F.current_version="0"
   with open(F.version_file,'w')as f:
    json.dump({'version':F.current_version},f)
 def process_version_url(F,D,K):
  T=D.replace("raw.githubusercontent.com","github.com") 
  T=T.replace("/","§",4) 
  T=T.replace("/","/latest-commit/",1) 
  T=T.replace("§","/",4) 
  T=T+K 
  return T
 def fetch_latest_code(F)->bool:
  X=urequests.get(F.firmware_url,timeout=20)
  if X.status_code==200:
   gc.collect()
   try:
    F.latest_code=X.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif X.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(F):
  with open('latest_code.py','w')as f:
   f.write(F.latest_code)
  F.current_version=F.latest_version
  with open(F.version_file,'w')as f:
   json.dump({'version':F.current_version},f)
  F.latest_code=None
  os.rename('latest_code.py',F.filename)
 def check_for_updates(F):
  gc.collect()
  W={"accept":"application/json"}
  X=urequests.get(F.version_url,headers=W,timeout=5)
  n=json.loads(X.text)
  F.latest_version=n['oid'] 
  e=True if F.current_version!=F.latest_version else False
  p="New ver: "+str(e)
  print(p) 
  return e
 def download_and_install_update_if_available(F):
  if F.check_for_updates():
   return F.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(F):
  if F.fetch_latest_code():
   F.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

