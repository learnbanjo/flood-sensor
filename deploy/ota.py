import urequests
import os
import gc
import json
L="1.0"
class OTAUpdater:
 def __init__(O,q,B):
  O.filename=B
  O.repo_url=q
  O.version_file=B+'_'+'ver.json'
  O.version_url=O.process_version_url(q,B) 
  O.firmware_url=q+B 
  if O.version_file in os.listdir():
   with open(O.version_file)as f:
    O.current_version=json.load(f)['version']
  else:
   O.current_version="0"
   with open(O.version_file,'w')as f:
    json.dump({'version':O.current_version},f)
 def process_version_url(O,q,B):
  p=q.replace("raw.githubusercontent.com","github.com") 
  p=p.replace("/","§",4) 
  p=p.replace("/","/latest-commit/",1) 
  p=p.replace("§","/",4) 
  p=p+B 
  return p
 def fetch_latest_code(O)->bool:
  a=urequests.get(O.firmware_url,timeout=20)
  if a.status_code==200:
   gc.collect()
   try:
    O.latest_code=a.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif a.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(O):
  with open('latest_code.py','w')as f:
   f.write(O.latest_code)
  O.current_version=O.latest_version
  with open(O.version_file,'w')as f:
   json.dump({'version':O.current_version},f)
  O.latest_code=None
  os.rename('latest_code.py',O.filename)
 def check_for_updates(O):
  gc.collect()
  o={"accept":"application/json"}
  a=urequests.get(O.version_url,headers=o,timeout=5)
  b=json.loads(a.text)
  O.latest_version=b['oid'] 
  P=True if O.current_version!=O.latest_version else False
  X="New ver: "+str(P)
  print(X) 
  return P
 def download_and_install_update_if_available(O):
  if O.check_for_updates():
   return O.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(O):
  if O.fetch_latest_code():
   O.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

