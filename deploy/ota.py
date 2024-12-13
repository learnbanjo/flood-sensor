import urequests
import os
import gc
import json
I="1.0"
class OTAUpdater:
 def __init__(o,v,a):
  o.filename=a
  o.repo_url=v
  o.version_file=a+'_'+'ver.json'
  o.version_url=o.process_version_url(v,a) 
  o.firmware_url=v+a 
  if o.version_file in os.listdir():
   with open(o.version_file)as f:
    o.current_version=json.load(f)['version']
  else:
   o.current_version="0"
   with open(o.version_file,'w')as f:
    json.dump({'version':o.current_version},f)
 def process_version_url(o,v,a):
  x=v.replace("raw.githubusercontent.com","github.com") 
  x=x.replace("/","§",4) 
  x=x.replace("/","/latest-commit/",1) 
  x=x.replace("§","/",4) 
  x=x+a 
  return x
 def fetch_latest_code(o)->bool:
  m=urequests.get(o.firmware_url,timeout=20)
  if m.status_code==200:
   gc.collect()
   try:
    o.latest_code=m.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif m.status_code==404:
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
  C={"accept":"application/json"}
  m=urequests.get(o.version_url,headers=C,timeout=5)
  n=json.loads(m.text)
  o.latest_version=n['oid'] 
  S=True if o.current_version!=o.latest_version else False
  c="New ver: "+str(S)
  print(c) 
  return S
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

