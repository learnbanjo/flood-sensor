import urequests
import os
import gc
import json
J="1.0"
class OTAUpdater:
 def __init__(C,Y,N):
  C.filename=N
  C.repo_url=Y
  C.version_file=N+'_'+'ver.json'
  C.version_url=C.process_version_url(Y,N) 
  C.firmware_url=Y+N 
  if C.version_file in os.listdir():
   with open(C.version_file)as f:
    C.current_version=json.load(f)['version']
  else:
   C.current_version="0"
   with open(C.version_file,'w')as f:
    json.dump({'version':C.current_version},f)
 def process_version_url(C,Y,N):
  m=Y.replace("raw.githubusercontent.com","github.com") 
  m=m.replace("/","§",4) 
  m=m.replace("/","/latest-commit/",1) 
  m=m.replace("§","/",4) 
  m=m+N 
  return m
 def fetch_latest_code(C)->bool:
  s=urequests.get(C.firmware_url,timeout=20)
  if s.status_code==200:
   gc.collect()
   try:
    C.latest_code=s.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif s.status_code==404:
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
  c={"accept":"application/json"}
  s=urequests.get(C.version_url,headers=c,timeout=5)
  x=json.loads(s.text)
  C.latest_version=x['oid'] 
  A=True if C.current_version!=C.latest_version else False
  R="New ver: "+str(A)
  print(R) 
  return A
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

