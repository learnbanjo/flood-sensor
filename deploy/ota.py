import urequests
import os
import gc
import json
K="1.0"
class OTAUpdater:
 def __init__(e,l,x):
  e.filename=x
  e.repo_url=l
  e.version_file=x+'_'+'ver.json'
  e.version_url=e.process_version_url(l,x) 
  e.firmware_url=l+x 
  if e.version_file in os.listdir():
   with open(e.version_file)as f:
    e.current_version=json.load(f)['version']
  else:
   e.current_version="0"
   with open(e.version_file,'w')as f:
    json.dump({'version':e.current_version},f)
 def process_version_url(e,l,x):
  Q=l.replace("raw.githubusercontent.com","github.com") 
  Q=Q.replace("/","§",4) 
  Q=Q.replace("/","/latest-commit/",1) 
  Q=Q.replace("§","/",4) 
  Q=Q+x 
  return Q
 def fetch_latest_code(e)->bool:
  g=urequests.get(e.firmware_url,timeout=20)
  if g.status_code==200:
   gc.collect()
   try:
    e.latest_code=g.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif g.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(e):
  with open('latest_code.py','w')as f:
   f.write(e.latest_code)
  e.current_version=e.latest_version
  with open(e.version_file,'w')as f:
   json.dump({'version':e.current_version},f)
  e.latest_code=None
  os.rename('latest_code.py',e.filename)
 def check_for_updates(e):
  gc.collect()
  j={"accept":"application/json"}
  g=urequests.get(e.version_url,headers=j,timeout=5)
  n=json.loads(g.text)
  e.latest_version=n['oid'] 
  P=True if e.current_version!=e.latest_version else False
  o="New ver: "+str(P)
  print(o) 
  return P
 def download_and_install_update_if_available(e):
  if e.check_for_updates():
   return e.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(e):
  if e.fetch_latest_code():
   e.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

