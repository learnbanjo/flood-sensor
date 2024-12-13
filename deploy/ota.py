import urequests
import os
import gc
import json
G="1.0"
class OTAUpdater:
 def __init__(F,c,J):
  F.filename=J
  F.repo_url=c
  F.version_file=J+'_'+'ver.json'
  F.version_url=F.process_version_url(c,J) 
  F.firmware_url=c+J 
  if F.version_file in os.listdir():
   with open(F.version_file)as f:
    F.current_version=json.load(f)['version']
  else:
   F.current_version="0"
   with open(F.version_file,'w')as f:
    json.dump({'version':F.current_version},f)
 def process_version_url(F,c,J):
  C=c.replace("raw.githubusercontent.com","github.com") 
  C=C.replace("/","§",4) 
  C=C.replace("/","/latest-commit/",1) 
  C=C.replace("§","/",4) 
  C=C+J 
  return C
 def fetch_latest_code(F)->bool:
  Q=urequests.get(F.firmware_url,timeout=20)
  if Q.status_code==200:
   gc.collect()
   try:
    F.latest_code=Q.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif Q.status_code==404:
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
  A={"accept":"application/json"}
  Q=urequests.get(F.version_url,headers=A,timeout=5)
  z=json.loads(Q.text)
  F.latest_version=z['oid'] 
  e=True if F.current_version!=F.latest_version else False
  l="New ver: "+str(e)
  print(l) 
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

