import urequests
import os
import gc
import json
R="1.0"
class OTAUpdater:
 def __init__(n,J,S):
  n.filename=S
  n.repo_url=J
  n.version_file=S+'_'+'ver.json'
  n.version_url=n.process_version_url(J,S) 
  n.firmware_url=J+S 
  if n.version_file in os.listdir():
   with open(n.version_file)as f:
    n.current_version=json.load(f)['version']
  else:
   n.current_version="0"
   with open(n.version_file,'w')as f:
    json.dump({'version':n.current_version},f)
 def process_version_url(n,J,S):
  o=J.replace("raw.githubusercontent.com","github.com") 
  o=o.replace("/","§",4) 
  o=o.replace("/","/latest-commit/",1) 
  o=o.replace("§","/",4) 
  o=o+S 
  return o
 def fetch_latest_code(n)->bool:
  w=urequests.get(n.firmware_url,timeout=20)
  if w.status_code==200:
   gc.collect()
   try:
    n.latest_code=w.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif w.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(n):
  with open('latest_code.py','w')as f:
   f.write(n.latest_code)
  n.current_version=n.latest_version
  with open(n.version_file,'w')as f:
   json.dump({'version':n.current_version},f)
  n.latest_code=None
  os.rename('latest_code.py',n.filename)
 def check_for_updates(n):
  gc.collect()
  E={"accept":"application/json"}
  w=urequests.get(n.version_url,headers=E,timeout=5)
  U=json.loads(w.text)
  n.latest_version=U['oid'] 
  c=True if n.current_version!=n.latest_version else False
  r="New ver: "+str(c)
  print(r) 
  return c
 def download_and_install_update_if_available(n):
  if n.check_for_updates():
   return n.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(n):
  if n.fetch_latest_code():
   n.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

