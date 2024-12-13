import urequests
import os
import gc
import json
P="1.0"
class OTAUpdater:
 def __init__(F,m,v):
  F.filename=v
  F.repo_url=m
  F.version_file=v+'_'+'ver.json'
  F.version_url=F.process_version_url(m,v) 
  F.firmware_url=m+v 
  if F.version_file in os.listdir():
   with open(F.version_file)as f:
    F.current_version=json.load(f)['version']
  else:
   F.current_version="0"
   with open(F.version_file,'w')as f:
    json.dump({'version':F.current_version},f)
 def process_version_url(F,m,v):
  M=m.replace("raw.githubusercontent.com","github.com") 
  M=M.replace("/","§",4) 
  M=M.replace("/","/latest-commit/",1) 
  M=M.replace("§","/",4) 
  M=M+v 
  return M
 def fetch_latest_code(F)->bool:
  N=urequests.get(F.firmware_url,timeout=20)
  if N.status_code==200:
   gc.collect()
   try:
    F.latest_code=N.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif N.status_code==404:
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
  q={"accept":"application/json"}
  N=urequests.get(F.version_url,headers=q,timeout=5)
  d=json.loads(N.text)
  F.latest_version=d['oid'] 
  D=True if F.current_version!=F.latest_version else False
  c="New ver: "+str(D)
  print(c) 
  return D
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

