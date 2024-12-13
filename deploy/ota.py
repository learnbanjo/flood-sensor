import urequests
import os
import gc
import json
B="1.0"
class OTAUpdater:
 def __init__(y,b,n):
  y.filename=n
  y.repo_url=b
  y.version_file=n+'_'+'ver.json'
  y.version_url=y.process_version_url(b,n) 
  y.firmware_url=b+n 
  if y.version_file in os.listdir():
   with open(y.version_file)as f:
    y.current_version=json.load(f)['version']
  else:
   y.current_version="0"
   with open(y.version_file,'w')as f:
    json.dump({'version':y.current_version},f)
 def process_version_url(y,b,n):
  t=b.replace("raw.githubusercontent.com","github.com") 
  t=t.replace("/","§",4) 
  t=t.replace("/","/latest-commit/",1) 
  t=t.replace("§","/",4) 
  t=t+n 
  return t
 def fetch_latest_code(y)->bool:
  E=urequests.get(y.firmware_url,timeout=20)
  if E.status_code==200:
   gc.collect()
   try:
    y.latest_code=E.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif E.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(y):
  with open('latest_code.py','w')as f:
   f.write(y.latest_code)
  y.current_version=y.latest_version
  with open(y.version_file,'w')as f:
   json.dump({'version':y.current_version},f)
  y.latest_code=None
  os.rename('latest_code.py',y.filename)
 def check_for_updates(y):
  gc.collect()
  k={"accept":"application/json"}
  E=urequests.get(y.version_url,headers=k,timeout=5)
  L=json.loads(E.text)
  y.latest_version=L['oid'] 
  K=True if y.current_version!=y.latest_version else False
  i="New ver: "+str(K)
  print(i) 
  return K
 def download_and_install_update_if_available(y):
  if y.check_for_updates():
   return y.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(y):
  if y.fetch_latest_code():
   y.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

