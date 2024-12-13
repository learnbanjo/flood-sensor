import urequests
import os
import gc
import json
E="1.0"
class OTAUpdater:
 def __init__(X,A,c):
  X.filename=c
  X.repo_url=A
  X.version_file=c+'_'+'ver.json'
  X.version_url=X.process_version_url(A,c) 
  X.firmware_url=A+c 
  if X.version_file in os.listdir():
   with open(X.version_file)as f:
    X.current_version=json.load(f)['version']
  else:
   X.current_version="0"
   with open(X.version_file,'w')as f:
    json.dump({'version':X.current_version},f)
 def process_version_url(X,A,c):
  V=A.replace("raw.githubusercontent.com","github.com") 
  V=V.replace("/","§",4) 
  V=V.replace("/","/latest-commit/",1) 
  V=V.replace("§","/",4) 
  V=V+c 
  return V
 def fetch_latest_code(X)->bool:
  M=urequests.get(X.firmware_url,timeout=20)
  if M.status_code==200:
   gc.collect()
   try:
    X.latest_code=M.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif M.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(X):
  with open('latest_code.py','w')as f:
   f.write(X.latest_code)
  X.current_version=X.latest_version
  with open(X.version_file,'w')as f:
   json.dump({'version':X.current_version},f)
  X.latest_code=None
  os.rename('latest_code.py',X.filename)
 def check_for_updates(X):
  gc.collect()
  L={"accept":"application/json"}
  M=urequests.get(X.version_url,headers=L,timeout=5)
  r=json.loads(M.text)
  X.latest_version=r['oid'] 
  u=True if X.current_version!=X.latest_version else False
  t="New ver: "+str(u)
  print(t) 
  return u
 def download_and_install_update_if_available(X):
  if X.check_for_updates():
   return X.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(X):
  if X.fetch_latest_code():
   X.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

