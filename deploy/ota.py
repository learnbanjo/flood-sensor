import urequests
import os
import gc
import json
c="1.0"
class OTAUpdater:
 def __init__(b,v,p):
  b.filename=p
  b.repo_url=v
  b.version_file=p+'_'+'ver.json'
  b.version_url=b.process_version_url(v,p) 
  b.firmware_url=v+p 
  if b.version_file in os.listdir():
   with open(b.version_file)as f:
    b.current_version=json.load(f)['version']
  else:
   b.current_version="0"
   with open(b.version_file,'w')as f:
    json.dump({'version':b.current_version},f)
 def process_version_url(b,v,p):
  O=v.replace("raw.githubusercontent.com","github.com") 
  O=O.replace("/","§",4) 
  O=O.replace("/","/latest-commit/",1) 
  O=O.replace("§","/",4) 
  O=O+p 
  return O
 def fetch_latest_code(b)->bool:
  S=urequests.get(b.firmware_url,timeout=20)
  if S.status_code==200:
   gc.collect()
   try:
    b.latest_code=S.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif S.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(b):
  with open('latest_code.py','w')as f:
   f.write(b.latest_code)
  b.current_version=b.latest_version
  with open(b.version_file,'w')as f:
   json.dump({'version':b.current_version},f)
  b.latest_code=None
  os.rename('latest_code.py',b.filename)
 def check_for_updates(b):
  gc.collect()
  J={"accept":"application/json"}
  S=urequests.get(b.version_url,headers=J,timeout=5)
  T=json.loads(S.text)
  b.latest_version=T['oid'] 
  R=True if b.current_version!=b.latest_version else False
  j="New ver: "+str(R)
  print(j) 
  return R
 def download_and_install_update_if_available(b):
  if b.check_for_updates():
   return b.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(b):
  if b.fetch_latest_code():
   b.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

