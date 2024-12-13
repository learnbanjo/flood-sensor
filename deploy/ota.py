import urequests
import os
import gc
import json
g="1.0"
class OTAUpdater:
 def __init__(z,H,a):
  z.filename=a
  z.repo_url=H
  z.version_file=a+'_'+'ver.json'
  z.version_url=z.process_version_url(H,a) 
  z.firmware_url=H+a 
  if z.version_file in os.listdir():
   with open(z.version_file)as f:
    z.current_version=json.load(f)['version']
  else:
   z.current_version="0"
   with open(z.version_file,'w')as f:
    json.dump({'version':z.current_version},f)
 def process_version_url(z,H,a):
  C=H.replace("raw.githubusercontent.com","github.com") 
  C=C.replace("/","§",4) 
  C=C.replace("/","/latest-commit/",1) 
  C=C.replace("§","/",4) 
  C=C+a 
  return C
 def fetch_latest_code(z)->bool:
  L=urequests.get(z.firmware_url,timeout=20)
  if L.status_code==200:
   gc.collect()
   try:
    z.latest_code=L.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif L.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(z):
  with open('latest_code.py','w')as f:
   f.write(z.latest_code)
  z.current_version=z.latest_version
  with open(z.version_file,'w')as f:
   json.dump({'version':z.current_version},f)
  z.latest_code=None
  os.rename('latest_code.py',z.filename)
 def check_for_updates(z):
  gc.collect()
  j={"accept":"application/json"}
  L=urequests.get(z.version_url,headers=j,timeout=5)
  y=json.loads(L.text)
  z.latest_version=y['oid'] 
  M=True if z.current_version!=z.latest_version else False
  R="New ver: "+str(M)
  print(R) 
  return M
 def download_and_install_update_if_available(z):
  if z.check_for_updates():
   return z.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(z):
  if z.fetch_latest_code():
   z.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

