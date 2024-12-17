import urequests
import os
import gc
import json
B="1.0"
class OTAUpdater:
 def __init__(O,m,f):
  O.filename=f
  O.repo_url=m
  O.version_file=f+'_'+'ver.json'
  O.version_url=O.process_version_url(m,f) 
  O.firmware_url=m+f 
  print("Version URL is ",O.version_url)
  print("Firmware URL is ",O.firmware_url)
  if O.version_file in os.listdir():
   with open(O.version_file)as f:
    O.current_version=json.load(f)['version']
   e="Current "+O.filename+" is "+O.current_version
   print("version message ",e)
  else:
   print("No version file")
   O.current_version="0"
   with open(O.version_file,'w')as f:
    json.dump({'version':O.current_version},f)
 def process_version_url(O,m,f):
  W=m.replace("raw.githubusercontent.com","github.com") 
  W=W.replace("/","§",4) 
  W=W.replace("/","/latest-commit/",1) 
  W=W.replace("§","/",4) 
  W=W+f 
  return W
 def fetch_latest_code(O)->bool:
  r=urequests.get(O.firmware_url,timeout=20)
  if r.status_code==200:
   gc.collect()
   try:
    O.latest_code=r.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif r.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(O):
  with open('latest_code.py','w')as f:
   f.write(O.latest_code)
  O.current_version=O.latest_version
  with open(O.version_file,'w')as f:
   json.dump({'version':O.current_version},f)
  O.latest_code=None
  os.rename('latest_code.py',O.filename)
 def check_for_updates(O):
  print('Checking for latest version...')
  gc.collect()
  U={"accept":"application/json"}
  r=urequests.get(O.version_url,headers=U,timeout=5)
  J=json.loads(r.text)
  O.latest_version=J['oid'] 
  n=True if O.current_version!=O.latest_version else False
  S="New ver: "+str(n)
  print(S) 
  return n
 def download_and_install_update_if_available(O):
  if O.check_for_updates():
   return O.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(O):
  if O.fetch_latest_code():
   O.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

