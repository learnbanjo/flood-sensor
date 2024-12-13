import urequests
import os
import gc
import json
y="1.0"
class OTAUpdater:
 def __init__(C,a,D):
  C.filename=D
  C.repo_url=a
  C.version_file=D+'_'+'ver.json'
  C.version_url=C.process_version_url(a,D) 
  C.firmware_url=a+D 
  if C.version_file in os.listdir():
   with open(C.version_file)as f:
    C.current_version=json.load(f)['version']
  else:
   C.current_version="0"
   with open(C.version_file,'w')as f:
    json.dump({'version':C.current_version},f)
 def process_version_url(C,a,D):
  P=a.replace("raw.githubusercontent.com","github.com") 
  P=P.replace("/","§",4) 
  P=P.replace("/","/latest-commit/",1) 
  P=P.replace("§","/",4) 
  P=P+D 
  return P
 def fetch_latest_code(C)->bool:
  N=urequests.get(C.firmware_url,timeout=20)
  if N.status_code==200:
   gc.collect()
   try:
    C.latest_code=N.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif N.status_code==404:
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
  S={"accept":"application/json"}
  N=urequests.get(C.version_url,headers=S,timeout=5)
  n=json.loads(N.text)
  C.latest_version=n['oid'] 
  R=True if C.current_version!=C.latest_version else False
  T="New ver: "+str(R)
  print(T) 
  return R
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

