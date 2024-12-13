import urequests
import os
import gc
import json
F="1.0"
class OTAUpdater:
 def __init__(U,M,v):
  U.filename=v
  U.repo_url=M
  U.version_file=v+'_'+'ver.json'
  U.version_url=U.process_version_url(M,v) 
  U.firmware_url=M+v 
  if U.version_file in os.listdir():
   with open(U.version_file)as f:
    U.current_version=json.load(f)['version']
  else:
   U.current_version="0"
   with open(U.version_file,'w')as f:
    json.dump({'version':U.current_version},f)
 def process_version_url(U,M,v):
  C=M.replace("raw.githubusercontent.com","github.com") 
  C=C.replace("/","§",4) 
  C=C.replace("/","/latest-commit/",1) 
  C=C.replace("§","/",4) 
  C=C+v 
  return C
 def fetch_latest_code(U)->bool:
  J=urequests.get(U.firmware_url,timeout=20)
  if J.status_code==200:
   gc.collect()
   try:
    U.latest_code=J.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif J.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(U):
  with open('latest_code.py','w')as f:
   f.write(U.latest_code)
  U.current_version=U.latest_version
  with open(U.version_file,'w')as f:
   json.dump({'version':U.current_version},f)
  U.latest_code=None
  os.rename('latest_code.py',U.filename)
 def check_for_updates(U):
  gc.collect()
  q={"accept":"application/json"}
  J=urequests.get(U.version_url,headers=q,timeout=5)
  h=json.loads(J.text)
  U.latest_version=h['oid'] 
  N=True if U.current_version!=U.latest_version else False
  K="New ver: "+str(N)
  print(K) 
  return N
 def download_and_install_update_if_available(U):
  if U.check_for_updates():
   return U.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(U):
  if U.fetch_latest_code():
   U.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

