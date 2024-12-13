import urequests
import os
import gc
import json
P="1.0"
class OTAUpdater:
 def __init__(x,J,T):
  x.filename=T
  x.repo_url=J
  x.version_file=T+'_'+'ver.json'
  x.version_url=x.process_version_url(J,T) 
  x.firmware_url=J+T 
  if x.version_file in os.listdir():
   with open(x.version_file)as f:
    x.current_version=json.load(f)['version']
  else:
   x.current_version="0"
   with open(x.version_file,'w')as f:
    json.dump({'version':x.current_version},f)
 def process_version_url(x,J,T):
  e=J.replace("raw.githubusercontent.com","github.com") 
  e=e.replace("/","§",4) 
  e=e.replace("/","/latest-commit/",1) 
  e=e.replace("§","/",4) 
  e=e+T 
  return e
 def fetch_latest_code(x)->bool:
  U=urequests.get(x.firmware_url,timeout=20)
  if U.status_code==200:
   gc.collect()
   try:
    x.latest_code=U.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif U.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(x):
  with open('latest_code.py','w')as f:
   f.write(x.latest_code)
  x.current_version=x.latest_version
  with open(x.version_file,'w')as f:
   json.dump({'version':x.current_version},f)
  x.latest_code=None
  os.rename('latest_code.py',x.filename)
 def check_for_updates(x):
  gc.collect()
  k={"accept":"application/json"}
  U=urequests.get(x.version_url,headers=k,timeout=5)
  q=json.loads(U.text)
  x.latest_version=q['oid'] 
  y=True if x.current_version!=x.latest_version else False
  i="New ver: "+str(y)
  print(i) 
  return y
 def download_and_install_update_if_available(x):
  if x.check_for_updates():
   return x.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(x):
  if x.fetch_latest_code():
   x.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

