import urequests
import os
import gc
import json
T="1.0"
class OTAUpdater:
 def __init__(p,k,j):
  p.filename=j
  p.repo_url=k
  p.version_file=j+'_'+'ver.json'
  p.version_url=p.process_version_url(k,j) 
  p.firmware_url=k+j 
  if p.version_file in os.listdir():
   with open(p.version_file)as f:
    p.current_version=json.load(f)['version']
  else:
   p.current_version="0"
   with open(p.version_file,'w')as f:
    json.dump({'version':p.current_version},f)
 def process_version_url(p,k,j):
  R=k.replace("raw.githubusercontent.com","github.com") 
  R=R.replace("/","§",4) 
  R=R.replace("/","/latest-commit/",1) 
  R=R.replace("§","/",4) 
  R=R+j 
  return R
 def fetch_latest_code(p)->bool:
  K=urequests.get(p.firmware_url,timeout=20)
  if K.status_code==200:
   gc.collect()
   try:
    p.latest_code=K.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif K.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(p):
  with open('latest_code.py','w')as f:
   f.write(p.latest_code)
  p.current_version=p.latest_version
  with open(p.version_file,'w')as f:
   json.dump({'version':p.current_version},f)
  p.latest_code=None
  os.rename('latest_code.py',p.filename)
 def check_for_updates(p):
  gc.collect()
  w={"accept":"application/json"}
  K=urequests.get(p.version_url,headers=w,timeout=5)
  J=json.loads(K.text)
  p.latest_version=J['oid'] 
  Y=True if p.current_version!=p.latest_version else False
  c="New ver: "+str(Y)
  print(c) 
  return Y
 def download_and_install_update_if_available(p):
  if p.check_for_updates():
   return p.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(p):
  if p.fetch_latest_code():
   p.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

