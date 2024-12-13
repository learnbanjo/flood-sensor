import urequests
import os
import gc
import json
k="1.0"
class OTAUpdater:
 def __init__(s,K,n):
  s.filename=n
  s.repo_url=K
  s.version_file=n+'_'+'ver.json'
  s.version_url=s.process_version_url(K,n) 
  s.firmware_url=K+n 
  if s.version_file in os.listdir():
   with open(s.version_file)as f:
    s.current_version=json.load(f)['version']
  else:
   s.current_version="0"
   with open(s.version_file,'w')as f:
    json.dump({'version':s.current_version},f)
 def process_version_url(s,K,n):
  h=K.replace("raw.githubusercontent.com","github.com") 
  h=h.replace("/","§",4) 
  h=h.replace("/","/latest-commit/",1) 
  h=h.replace("§","/",4) 
  h=h+n 
  return h
 def fetch_latest_code(s)->bool:
  f=urequests.get(s.firmware_url,timeout=20)
  if f.status_code==200:
   gc.collect()
   try:
    s.latest_code=f.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif f.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(s):
  with open('latest_code.py','w')as f:
   f.write(s.latest_code)
  s.current_version=s.latest_version
  with open(s.version_file,'w')as f:
   json.dump({'version':s.current_version},f)
  s.latest_code=None
  os.rename('latest_code.py',s.filename)
 def check_for_updates(s):
  gc.collect()
  J={"accept":"application/json"}
  f=urequests.get(s.version_url,headers=J,timeout=5)
  E=json.loads(f.text)
  s.latest_version=E['oid'] 
  a=True if s.current_version!=s.latest_version else False
  H="New ver: "+str(a)
  print(H) 
  return a
 def download_and_install_update_if_available(s):
  if s.check_for_updates():
   return s.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(s):
  if s.fetch_latest_code():
   s.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

