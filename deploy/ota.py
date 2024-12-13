import urequests
import os
import gc
import json
N="1.0"
class OTAUpdater:
 def __init__(v,C,s):
  v.filename=s
  v.repo_url=C
  v.version_file=s+'_'+'ver.json'
  v.version_url=v.process_version_url(C,s) 
  v.firmware_url=C+s 
  if v.version_file in os.listdir():
   with open(v.version_file)as f:
    v.current_version=json.load(f)['version']
  else:
   v.current_version="0"
   with open(v.version_file,'w')as f:
    json.dump({'version':v.current_version},f)
 def process_version_url(v,C,s):
  Y=C.replace("raw.githubusercontent.com","github.com") 
  Y=Y.replace("/","§",4) 
  Y=Y.replace("/","/latest-commit/",1) 
  Y=Y.replace("§","/",4) 
  Y=Y+s 
  return Y
 def fetch_latest_code(v)->bool:
  z=urequests.get(v.firmware_url,timeout=20)
  if z.status_code==200:
   gc.collect()
   try:
    v.latest_code=z.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif z.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(v):
  with open('latest_code.py','w')as f:
   f.write(v.latest_code)
  v.current_version=v.latest_version
  with open(v.version_file,'w')as f:
   json.dump({'version':v.current_version},f)
  v.latest_code=None
  os.rename('latest_code.py',v.filename)
 def check_for_updates(v):
  gc.collect()
  M={"accept":"application/json"}
  z=urequests.get(v.version_url,headers=M,timeout=5)
  W=json.loads(z.text)
  v.latest_version=W['oid'] 
  D=True if v.current_version!=v.latest_version else False
  q="New ver: "+str(D)
  print(q) 
  return D
 def download_and_install_update_if_available(v):
  if v.check_for_updates():
   return v.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(v):
  if v.fetch_latest_code():
   v.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

