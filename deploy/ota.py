import urequests
import os
import gc
import json
a="1.0"
class OTAUpdater:
 def __init__(i,y,t):
  i.filename=t
  i.repo_url=y
  i.version_file=t+'_'+'ver.json'
  i.version_url=i.process_version_url(y,t) 
  i.firmware_url=y+t 
  if i.version_file in os.listdir():
   with open(i.version_file)as f:
    i.current_version=json.load(f)['version']
  else:
   i.current_version="0"
   with open(i.version_file,'w')as f:
    json.dump({'version':i.current_version},f)
 def process_version_url(i,y,t):
  Y=y.replace("raw.githubusercontent.com","github.com") 
  Y=Y.replace("/","§",4) 
  Y=Y.replace("/","/latest-commit/",1) 
  Y=Y.replace("§","/",4) 
  Y=Y+t 
  return Y
 def fetch_latest_code(i)->bool:
  P=urequests.get(i.firmware_url,timeout=20)
  if P.status_code==200:
   gc.collect()
   try:
    i.latest_code=P.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif P.status_code==404:
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
  U={"accept":"application/json"}
  P=urequests.get(i.version_url,headers=U,timeout=5)
  r=json.loads(P.text)
  i.latest_version=r['oid'] 
  p=True if i.current_version!=i.latest_version else False
  A="New ver: "+str(p)
  print(A) 
  return p
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

