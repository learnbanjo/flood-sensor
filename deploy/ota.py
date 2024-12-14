import urequests
import os
import gc
import json
o="1.0"
class OTAUpdater:
 def __init__(I,g,r):
  I.filename=r
  I.repo_url=g
  I.version_file=r+'_'+'ver.json'
  I.version_url=I.process_version_url(g,r) 
  I.firmware_url=g+r 
  if I.version_file in os.listdir():
   with open(I.version_file)as f:
    I.current_version=json.load(f)['version']
  else:
   I.current_version="0"
   with open(I.version_file,'w')as f:
    json.dump({'version':I.current_version},f)
 def process_version_url(I,g,r):
  c=g.replace("raw.githubusercontent.com","github.com") 
  c=c.replace("/","§",4) 
  c=c.replace("/","/latest-commit/",1) 
  c=c.replace("§","/",4) 
  c=c+r 
  return c
 def fetch_latest_code(I)->bool:
  V=urequests.get(I.firmware_url,timeout=20)
  if V.status_code==200:
   gc.collect()
   try:
    I.latest_code=V.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif V.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(I):
  with open('latest_code.py','w')as f:
   f.write(I.latest_code)
  I.current_version=I.latest_version
  with open(I.version_file,'w')as f:
   json.dump({'version':I.current_version},f)
  I.latest_code=None
  os.rename('latest_code.py',I.filename)
 def check_for_updates(I):
  gc.collect()
  d={"accept":"application/json"}
  V=urequests.get(I.version_url,headers=d,timeout=5)
  U=json.loads(V.text)
  I.latest_version=U['oid'] 
  l=True if I.current_version!=I.latest_version else False
  M="New ver: "+str(l)
  print(M) 
  return l
 def download_and_install_update_if_available(I):
  if I.check_for_updates():
   return I.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(I):
  if I.fetch_latest_code():
   I.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

