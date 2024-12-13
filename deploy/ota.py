import urequests
import os
import gc
import json
y="1.0"
class OTAUpdater:
 def __init__(J,o,T):
  J.filename=T
  J.repo_url=o
  J.version_file=T+'_'+'ver.json'
  J.version_url=J.process_version_url(o,T) 
  J.firmware_url=o+T 
  if J.version_file in os.listdir():
   with open(J.version_file)as f:
    J.current_version=json.load(f)['version']
  else:
   J.current_version="0"
   with open(J.version_file,'w')as f:
    json.dump({'version':J.current_version},f)
 def process_version_url(J,o,T):
  U=o.replace("raw.githubusercontent.com","github.com") 
  U=U.replace("/","§",4) 
  U=U.replace("/","/latest-commit/",1) 
  U=U.replace("§","/",4) 
  U=U+T 
  return U
 def fetch_latest_code(J)->bool:
  w=urequests.get(J.firmware_url,timeout=20)
  if w.status_code==200:
   gc.collect()
   try:
    J.latest_code=w.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif w.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(J):
  with open('latest_code.py','w')as f:
   f.write(J.latest_code)
  J.current_version=J.latest_version
  with open(J.version_file,'w')as f:
   json.dump({'version':J.current_version},f)
  J.latest_code=None
  os.rename('latest_code.py',J.filename)
 def check_for_updates(J):
  gc.collect()
  N={"accept":"application/json"}
  w=urequests.get(J.version_url,headers=N,timeout=5)
  u=json.loads(w.text)
  J.latest_version=u['oid'] 
  v=True if J.current_version!=J.latest_version else False
  K="New ver: "+str(v)
  print(K) 
  return v
 def download_and_install_update_if_available(J):
  if J.check_for_updates():
   return J.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(J):
  if J.fetch_latest_code():
   J.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

