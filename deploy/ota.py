import urequests
import os
import gc
import json
E="1.0"
class OTAUpdater:
 def __init__(b,S,u):
  b.filename=u
  b.repo_url=S
  b.version_file=u+'_'+'ver.json'
  b.version_url=b.process_version_url(S,u) 
  b.firmware_url=S+u 
  if b.version_file in os.listdir():
   with open(b.version_file)as f:
    b.current_version=json.load(f)['version']
  else:
   b.current_version="0"
   with open(b.version_file,'w')as f:
    json.dump({'version':b.current_version},f)
 def process_version_url(b,S,u):
  W=S.replace("raw.githubusercontent.com","github.com") 
  W=W.replace("/","§",4) 
  W=W.replace("/","/latest-commit/",1) 
  W=W.replace("§","/",4) 
  W=W+u 
  return W
 def fetch_latest_code(b)->bool:
  a=urequests.get(b.firmware_url,timeout=20)
  if a.status_code==200:
   gc.collect()
   try:
    b.latest_code=a.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif a.status_code==404:
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
  M={"accept":"application/json"}
  a=urequests.get(b.version_url,headers=M,timeout=5)
  f=json.loads(a.text)
  b.latest_version=f['oid'] 
  C=True if b.current_version!=b.latest_version else False
  X="New ver: "+str(C)
  print(X) 
  return C
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

