import urequests
import os
import gc
import json
g="1.0"
class OTAUpdater:
 def __init__(e,c,j):
  e.filename=j
  e.repo_url=c
  e.version_file=j+'_'+'ver.json'
  e.version_url=e.process_version_url(c,j) 
  e.firmware_url=c+j 
  if e.version_file in os.listdir():
   with open(e.version_file)as f:
    e.current_version=json.load(f)['version']
  else:
   e.current_version="0"
   with open(e.version_file,'w')as f:
    json.dump({'version':e.current_version},f)
 def process_version_url(e,c,j):
  W=c.replace("raw.githubusercontent.com","github.com") 
  W=W.replace("/","§",4) 
  W=W.replace("/","/latest-commit/",1) 
  W=W.replace("§","/",4) 
  W=W+j 
  return W
 def fetch_latest_code(e)->bool:
  C=urequests.get(e.firmware_url,timeout=20)
  if C.status_code==200:
   gc.collect()
   try:
    e.latest_code=C.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif C.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(e):
  with open('latest_code.py','w')as f:
   f.write(e.latest_code)
  e.current_version=e.latest_version
  with open(e.version_file,'w')as f:
   json.dump({'version':e.current_version},f)
  e.latest_code=None
  os.rename('latest_code.py',e.filename)
 def check_for_updates(e):
  gc.collect()
  U={"accept":"application/json"}
  C=urequests.get(e.version_url,headers=U,timeout=5)
  K=json.loads(C.text)
  e.latest_version=K['oid'] 
  E=True if e.current_version!=e.latest_version else False
  q="New ver: "+str(E)
  print(q) 
  return E
 def download_and_install_update_if_available(e):
  if e.check_for_updates():
   return e.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(e):
  if e.fetch_latest_code():
   e.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

