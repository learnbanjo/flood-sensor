import urequests
import os
import gc
import json
l="1.0"
class OTAUpdater:
 def __init__(J,K,R):
  J.filename=R
  J.repo_url=K
  J.version_file=R+'_'+'ver.json'
  J.version_url=J.process_version_url(K,R) 
  J.firmware_url=K+R 
  if J.version_file in os.listdir():
   with open(J.version_file)as f:
    J.current_version=json.load(f)['version']
  else:
   J.current_version="0"
   with open(J.version_file,'w')as f:
    json.dump({'version':J.current_version},f)
 def process_version_url(J,K,R):
  Y=K.replace("raw.githubusercontent.com","github.com") 
  Y=Y.replace("/","§",4) 
  Y=Y.replace("/","/latest-commit/",1) 
  Y=Y.replace("§","/",4) 
  Y=Y+R 
  return Y
 def fetch_latest_code(J)->bool:
  Q=urequests.get(J.firmware_url,timeout=20)
  if Q.status_code==200:
   gc.collect()
   try:
    J.latest_code=Q.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif Q.status_code==404:
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
  B={"accept":"application/json"}
  Q=urequests.get(J.version_url,headers=B,timeout=5)
  j=json.loads(Q.text)
  J.latest_version=j['oid'] 
  S=True if J.current_version!=J.latest_version else False
  o="New ver: "+str(S)
  print(o) 
  return S
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

