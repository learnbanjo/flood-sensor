import urequests
import os
import gc
import json
e="1.0"
class OTAUpdater:
 def __init__(i,n,T):
  i.filename=T
  i.repo_url=n
  i.version_file=T+'_'+'ver.json'
  i.version_url=i.process_version_url(n,T) 
  i.firmware_url=n+T 
  if i.version_file in os.listdir():
   with open(i.version_file)as f:
    i.current_version=json.load(f)['version']
  else:
   i.current_version="0"
   with open(i.version_file,'w')as f:
    json.dump({'version':i.current_version},f)
 def process_version_url(i,n,T):
  K=n.replace("raw.githubusercontent.com","github.com") 
  K=K.replace("/","§",4) 
  K=K.replace("/","/latest-commit/",1) 
  K=K.replace("§","/",4) 
  K=K+T 
  return K
 def fetch_latest_code(i)->bool:
  h=urequests.get(i.firmware_url,timeout=20)
  if h.status_code==200:
   gc.collect()
   try:
    i.latest_code=h.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif h.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(i):
  with open('latest_code.py','w')as f:
   f.write(i.latest_code)
  i.current_version=i.latest_version
  with open(i.version_file,'w')as f:
   json.dump({'version':i.current_version},f)
  i.latest_code=None
  os.rename('latest_code.py',i.filename)
 def check_for_updates(i):
  gc.collect()
  m={"accept":"application/json"}
  h=urequests.get(i.version_url,headers=m,timeout=5)
  R=json.loads(h.text)
  i.latest_version=R['oid'] 
  P=True if i.current_version!=i.latest_version else False
  a="New ver: "+str(P)
  print(a) 
  return P
 def download_and_install_update_if_available(i):
  if i.check_for_updates():
   return i.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(i):
  if i.fetch_latest_code():
   i.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

