import urequests
import os
import gc
import json
g="1.0"
class OTAUpdater:
 def __init__(W,V,B):
  W.filename=B
  W.repo_url=V
  W.version_file=B+'_'+'ver.json'
  W.version_url=W.process_version_url(V,B) 
  W.firmware_url=V+B 
  if W.version_file in os.listdir():
   with open(W.version_file)as f:
    W.current_version=json.load(f)['version']
  else:
   W.current_version="0"
   with open(W.version_file,'w')as f:
    json.dump({'version':W.current_version},f)
 def process_version_url(W,V,B):
  I=V.replace("raw.githubusercontent.com","github.com") 
  I=I.replace("/","§",4) 
  I=I.replace("/","/latest-commit/",1) 
  I=I.replace("§","/",4) 
  I=I+B 
  return I
 def fetch_latest_code(W)->bool:
  z=urequests.get(W.firmware_url,timeout=20)
  if z.status_code==200:
   gc.collect()
   try:
    W.latest_code=z.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif z.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(W):
  with open('latest_code.py','w')as f:
   f.write(W.latest_code)
  W.current_version=W.latest_version
  with open(W.version_file,'w')as f:
   json.dump({'version':W.current_version},f)
  W.latest_code=None
  os.rename('latest_code.py',W.filename)
 def check_for_updates(W):
  gc.collect()
  Q={"accept":"application/json"}
  z=urequests.get(W.version_url,headers=Q,timeout=5)
  j=json.loads(z.text)
  W.latest_version=j['oid'] 
  M=True if W.current_version!=W.latest_version else False
  L="New ver: "+str(M)
  print(L) 
  return M
 def download_and_install_update_if_available(W):
  if W.check_for_updates():
   return W.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(W):
  if W.fetch_latest_code():
   W.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

