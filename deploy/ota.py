import urequests
import os
import gc
import json
q="1.0"
class OTAUpdater:
 def __init__(e,F,S):
  e.filename=S
  e.repo_url=F
  e.version_file=S+'_'+'ver.json'
  e.version_url=e.process_version_url(F,S) 
  e.firmware_url=F+S 
  if e.version_file in os.listdir():
   with open(e.version_file)as f:
    e.current_version=json.load(f)['version']
  else:
   e.current_version="0"
   with open(e.version_file,'w')as f:
    json.dump({'version':e.current_version},f)
 def process_version_url(e,F,S):
  g=F.replace("raw.githubusercontent.com","github.com") 
  g=g.replace("/","§",4) 
  g=g.replace("/","/latest-commit/",1) 
  g=g.replace("§","/",4) 
  g=g+S 
  return g
 def fetch_latest_code(e)->bool:
  n=urequests.get(e.firmware_url,timeout=20)
  if n.status_code==200:
   gc.collect()
   try:
    e.latest_code=n.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif n.status_code==404:
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
  a={"accept":"application/json"}
  n=urequests.get(e.version_url,headers=a,timeout=5)
  H=json.loads(n.text)
  e.latest_version=H['oid'] 
  w=True if e.current_version!=e.latest_version else False
  Q="New ver: "+str(w)
  print(Q) 
  return w
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

