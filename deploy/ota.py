import urequests
import os
import gc
import json
T="1.0"
class OTAUpdater:
 def __init__(b,w,Y):
  b.filename=Y
  b.repo_url=w
  b.version_file=Y+'_'+'ver.json'
  b.version_url=b.process_version_url(w,Y) 
  b.firmware_url=w+Y 
  if b.version_file in os.listdir():
   with open(b.version_file)as f:
    b.current_version=json.load(f)['version']
  else:
   b.current_version="0"
   with open(b.version_file,'w')as f:
    json.dump({'version':b.current_version},f)
 def process_version_url(b,w,Y):
  i=w.replace("raw.githubusercontent.com","github.com") 
  i=i.replace("/","§",4) 
  i=i.replace("/","/latest-commit/",1) 
  i=i.replace("§","/",4) 
  i=i+Y 
  return i
 def fetch_latest_code(b)->bool:
  x=urequests.get(b.firmware_url,timeout=20)
  if x.status_code==200:
   gc.collect()
   try:
    b.latest_code=x.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif x.status_code==404:
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
  q={"accept":"application/json"}
  x=urequests.get(b.version_url,headers=q,timeout=5)
  U=json.loads(x.text)
  b.latest_version=U['oid'] 
  j=True if b.current_version!=b.latest_version else False
  A="New ver: "+str(j)
  print(A) 
  return j
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

