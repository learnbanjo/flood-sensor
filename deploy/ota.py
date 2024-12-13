import urequests
import os
import gc
import json
u="1.0"
class OTAUpdater:
 def __init__(F,N,O):
  F.filename=O
  F.repo_url=N
  F.version_file=O+'_'+'ver.json'
  F.version_url=F.process_version_url(N,O) 
  F.firmware_url=N+O 
  if F.version_file in os.listdir():
   with open(F.version_file)as f:
    F.current_version=json.load(f)['version']
  else:
   F.current_version="0"
   with open(F.version_file,'w')as f:
    json.dump({'version':F.current_version},f)
 def process_version_url(F,N,O):
  q=N.replace("raw.githubusercontent.com","github.com") 
  q=q.replace("/","§",4) 
  q=q.replace("/","/latest-commit/",1) 
  q=q.replace("§","/",4) 
  q=q+O 
  return q
 def fetch_latest_code(F)->bool:
  r=urequests.get(F.firmware_url,timeout=20)
  if r.status_code==200:
   gc.collect()
   try:
    F.latest_code=r.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif r.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(F):
  with open('latest_code.py','w')as f:
   f.write(F.latest_code)
  F.current_version=F.latest_version
  with open(F.version_file,'w')as f:
   json.dump({'version':F.current_version},f)
  F.latest_code=None
  os.rename('latest_code.py',F.filename)
 def check_for_updates(F):
  gc.collect()
  M={"accept":"application/json"}
  r=urequests.get(F.version_url,headers=M,timeout=5)
  n=json.loads(r.text)
  F.latest_version=n['oid'] 
  w=True if F.current_version!=F.latest_version else False
  I="New ver: "+str(w)
  print(I) 
  return w
 def download_and_install_update_if_available(F):
  if F.check_for_updates():
   return F.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(F):
  if F.fetch_latest_code():
   F.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

