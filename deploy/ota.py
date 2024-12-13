import urequests
import os
import gc
import json
a="1.0"
class OTAUpdater:
 def __init__(B,p,b):
  B.filename=b
  B.repo_url=p
  B.version_file=b+'_'+'ver.json'
  B.version_url=B.process_version_url(p,b) 
  B.firmware_url=p+b 
  if B.version_file in os.listdir():
   with open(B.version_file)as f:
    B.current_version=json.load(f)['version']
  else:
   B.current_version="0"
   with open(B.version_file,'w')as f:
    json.dump({'version':B.current_version},f)
 def process_version_url(B,p,b):
  Y=p.replace("raw.githubusercontent.com","github.com") 
  Y=Y.replace("/","§",4) 
  Y=Y.replace("/","/latest-commit/",1) 
  Y=Y.replace("§","/",4) 
  Y=Y+b 
  return Y
 def fetch_latest_code(B)->bool:
  i=urequests.get(B.firmware_url,timeout=20)
  if i.status_code==200:
   gc.collect()
   try:
    B.latest_code=i.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif i.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(B):
  with open('latest_code.py','w')as f:
   f.write(B.latest_code)
  B.current_version=B.latest_version
  with open(B.version_file,'w')as f:
   json.dump({'version':B.current_version},f)
  B.latest_code=None
  os.rename('latest_code.py',B.filename)
 def check_for_updates(B):
  gc.collect()
  E={"accept":"application/json"}
  i=urequests.get(B.version_url,headers=E,timeout=5)
  O=json.loads(i.text)
  B.latest_version=O['oid'] 
  J=True if B.current_version!=B.latest_version else False
  v="New ver: "+str(J)
  print(v) 
  return J
 def download_and_install_update_if_available(B):
  if B.check_for_updates():
   return B.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(B):
  if B.fetch_latest_code():
   B.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

