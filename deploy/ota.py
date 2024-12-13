import urequests
import os
import gc
import json
o="1.0"
class OTAUpdater:
 def __init__(u,E,N):
  u.filename=N
  u.repo_url=E
  u.version_file=N+'_'+'ver.json'
  u.version_url=u.process_version_url(E,N) 
  u.firmware_url=E+N 
  if u.version_file in os.listdir():
   with open(u.version_file)as f:
    u.current_version=json.load(f)['version']
  else:
   u.current_version="0"
   with open(u.version_file,'w')as f:
    json.dump({'version':u.current_version},f)
 def process_version_url(u,E,N):
  O=E.replace("raw.githubusercontent.com","github.com") 
  O=O.replace("/","§",4) 
  O=O.replace("/","/latest-commit/",1) 
  O=O.replace("§","/",4) 
  O=O+N 
  return O
 def fetch_latest_code(u)->bool:
  J=urequests.get(u.firmware_url,timeout=20)
  if J.status_code==200:
   gc.collect()
   try:
    u.latest_code=J.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif J.status_code==404:
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
  z={"accept":"application/json"}
  J=urequests.get(u.version_url,headers=z,timeout=5)
  e=json.loads(J.text)
  u.latest_version=e['oid'] 
  j=True if u.current_version!=u.latest_version else False
  p="New ver: "+str(j)
  print(p) 
  return j
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

