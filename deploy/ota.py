import urequests
import os
import gc
import json
c="1.0"
class OTAUpdater:
 def __init__(X,r,i):
  X.filename=i
  X.repo_url=r
  X.version_file=i+'_'+'ver.json'
  X.version_url=X.process_version_url(r,i) 
  X.firmware_url=r+i 
  if X.version_file in os.listdir():
   with open(X.version_file)as f:
    X.current_version=json.load(f)['version']
  else:
   X.current_version="0"
   with open(X.version_file,'w')as f:
    json.dump({'version':X.current_version},f)
 def process_version_url(X,r,i):
  x=r.replace("raw.githubusercontent.com","github.com") 
  x=x.replace("/","§",4) 
  x=x.replace("/","/latest-commit/",1) 
  x=x.replace("§","/",4) 
  x=x+i 
  return x
 def fetch_latest_code(X)->bool:
  G=urequests.get(X.firmware_url,timeout=20)
  if G.status_code==200:
   gc.collect()
   try:
    X.latest_code=G.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif G.status_code==404:
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
  B={"accept":"application/json"}
  G=urequests.get(X.version_url,headers=B,timeout=5)
  U=json.loads(G.text)
  X.latest_version=U['oid'] 
  V=True if X.current_version!=X.latest_version else False
  T="New ver: "+str(V)
  print(T) 
  return V
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

