import urequests
import os
import gc
import json
a="1.0"
class OTAUpdater:
 def __init__(u,E,B):
  u.filename=B
  u.repo_url=E
  u.version_file=B+'_'+'ver.json'
  u.version_url=u.process_version_url(E,B) 
  u.firmware_url=E+B 
  if u.version_file in os.listdir():
   with open(u.version_file)as f:
    u.current_version=json.load(f)['version']
  else:
   u.current_version="0"
   with open(u.version_file,'w')as f:
    json.dump({'version':u.current_version},f)
 def process_version_url(u,E,B):
  A=E.replace("raw.githubusercontent.com","github.com") 
  A=A.replace("/","§",4) 
  A=A.replace("/","/latest-commit/",1) 
  A=A.replace("§","/",4) 
  A=A+B 
  return A
 def fetch_latest_code(u)->bool:
  o=urequests.get(u.firmware_url,timeout=20)
  if o.status_code==200:
   gc.collect()
   try:
    u.latest_code=o.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif o.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(u):
  with open('latest_code.py','w')as f:
   f.write(u.latest_code)
  u.current_version=u.latest_version
  with open(u.version_file,'w')as f:
   json.dump({'version':u.current_version},f)
  u.latest_code=None
  os.rename('latest_code.py',u.filename)
 def check_for_updates(u):
  gc.collect()
  e={"accept":"application/json"}
  o=urequests.get(u.version_url,headers=e,timeout=5)
  v=json.loads(o.text)
  u.latest_version=v['oid'] 
  i=True if u.current_version!=u.latest_version else False
  U="New ver: "+str(i)
  print(U) 
  return i
 def download_and_install_update_if_available(u):
  if u.check_for_updates():
   return u.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(u):
  if u.fetch_latest_code():
   u.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

