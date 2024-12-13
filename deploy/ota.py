import urequests
import os
import gc
import json
I="1.0"
class OTAUpdater:
 def __init__(o,c,O):
  o.filename=O
  o.repo_url=c
  o.version_file=O+'_'+'ver.json'
  o.version_url=o.process_version_url(c,O) 
  o.firmware_url=c+O 
  if o.version_file in os.listdir():
   with open(o.version_file)as f:
    o.current_version=json.load(f)['version']
  else:
   o.current_version="0"
   with open(o.version_file,'w')as f:
    json.dump({'version':o.current_version},f)
 def process_version_url(o,c,O):
  H=c.replace("raw.githubusercontent.com","github.com") 
  H=H.replace("/","§",4) 
  H=H.replace("/","/latest-commit/",1) 
  H=H.replace("§","/",4) 
  H=H+O 
  return H
 def fetch_latest_code(o)->bool:
  C=urequests.get(o.firmware_url,timeout=20)
  if C.status_code==200:
   gc.collect()
   try:
    o.latest_code=C.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif C.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(o):
  with open('latest_code.py','w')as f:
   f.write(o.latest_code)
  o.current_version=o.latest_version
  with open(o.version_file,'w')as f:
   json.dump({'version':o.current_version},f)
  o.latest_code=None
  os.rename('latest_code.py',o.filename)
 def check_for_updates(o):
  gc.collect()
  G={"accept":"application/json"}
  C=urequests.get(o.version_url,headers=G,timeout=5)
  v=json.loads(C.text)
  o.latest_version=v['oid'] 
  m=True if o.current_version!=o.latest_version else False
  T="New ver: "+str(m)
  print(T) 
  return m
 def download_and_install_update_if_available(o):
  if o.check_for_updates():
   return o.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(o):
  if o.fetch_latest_code():
   o.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

