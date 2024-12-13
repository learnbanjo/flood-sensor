import urequests
import os
import gc
import json
f="1.0"
class OTAUpdater:
 def __init__(K,R,W):
  K.filename=W
  K.repo_url=R
  K.version_file=W+'_'+'ver.json'
  K.version_url=K.process_version_url(R,W) 
  K.firmware_url=R+W 
  if K.version_file in os.listdir():
   with open(K.version_file)as f:
    K.current_version=json.load(f)['version']
  else:
   K.current_version="0"
   with open(K.version_file,'w')as f:
    json.dump({'version':K.current_version},f)
 def process_version_url(K,R,W):
  M=R.replace("raw.githubusercontent.com","github.com") 
  M=M.replace("/","§",4) 
  M=M.replace("/","/latest-commit/",1) 
  M=M.replace("§","/",4) 
  M=M+W 
  return M
 def fetch_latest_code(K)->bool:
  S=urequests.get(K.firmware_url,timeout=20)
  if S.status_code==200:
   gc.collect()
   try:
    K.latest_code=S.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif S.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(K):
  with open('latest_code.py','w')as f:
   f.write(K.latest_code)
  K.current_version=K.latest_version
  with open(K.version_file,'w')as f:
   json.dump({'version':K.current_version},f)
  K.latest_code=None
  os.rename('latest_code.py',K.filename)
 def check_for_updates(K):
  gc.collect()
  Q={"accept":"application/json"}
  S=urequests.get(K.version_url,headers=Q,timeout=5)
  z=json.loads(S.text)
  K.latest_version=z['oid'] 
  Y=True if K.current_version!=K.latest_version else False
  L="New ver: "+str(Y)
  print(L) 
  return Y
 def download_and_install_update_if_available(K):
  if K.check_for_updates():
   return K.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(K):
  if K.fetch_latest_code():
   K.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

