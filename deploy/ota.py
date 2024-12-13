import urequests
import os
import gc
import json
E="1.0"
class OTAUpdater:
 def __init__(C,k,j):
  C.filename=j
  C.repo_url=k
  C.version_file=j+'_'+'ver.json'
  C.version_url=C.process_version_url(k,j) 
  C.firmware_url=k+j 
  if C.version_file in os.listdir():
   with open(C.version_file)as f:
    C.current_version=json.load(f)['version']
  else:
   C.current_version="0"
   with open(C.version_file,'w')as f:
    json.dump({'version':C.current_version},f)
 def process_version_url(C,k,j):
  q=k.replace("raw.githubusercontent.com","github.com") 
  q=q.replace("/","§",4) 
  q=q.replace("/","/latest-commit/",1) 
  q=q.replace("§","/",4) 
  q=q+j 
  return q
 def fetch_latest_code(C)->bool:
  u=urequests.get(C.firmware_url,timeout=20)
  if u.status_code==200:
   gc.collect()
   try:
    C.latest_code=u.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif u.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(C):
  with open('latest_code.py','w')as f:
   f.write(C.latest_code)
  C.current_version=C.latest_version
  with open(C.version_file,'w')as f:
   json.dump({'version':C.current_version},f)
  C.latest_code=None
  os.rename('latest_code.py',C.filename)
 def check_for_updates(C):
  gc.collect()
  o={"accept":"application/json"}
  u=urequests.get(C.version_url,headers=o,timeout=5)
  d=json.loads(u.text)
  C.latest_version=d['oid'] 
  B=True if C.current_version!=C.latest_version else False
  h="New ver: "+str(B)
  print(h) 
  return B
 def download_and_install_update_if_available(C):
  if C.check_for_updates():
   return C.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(C):
  if C.fetch_latest_code():
   C.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

