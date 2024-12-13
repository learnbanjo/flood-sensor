import urequests
import os
import gc
import json
o="1.0"
class OTAUpdater:
 def __init__(B,h,w):
  B.filename=w
  B.repo_url=h
  B.version_file=w+'_'+'ver.json'
  B.version_url=B.process_version_url(h,w) 
  B.firmware_url=h+w 
  if B.version_file in os.listdir():
   with open(B.version_file)as f:
    B.current_version=json.load(f)['version']
  else:
   B.current_version="0"
   with open(B.version_file,'w')as f:
    json.dump({'version':B.current_version},f)
 def process_version_url(B,h,w):
  T=h.replace("raw.githubusercontent.com","github.com") 
  T=T.replace("/","§",4) 
  T=T.replace("/","/latest-commit/",1) 
  T=T.replace("§","/",4) 
  T=T+w 
  return T
 def fetch_latest_code(B)->bool:
  n=urequests.get(B.firmware_url,timeout=20)
  if n.status_code==200:
   gc.collect()
   try:
    B.latest_code=n.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif n.status_code==404:
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
  O={"accept":"application/json"}
  n=urequests.get(B.version_url,headers=O,timeout=5)
  z=json.loads(n.text)
  B.latest_version=z['oid'] 
  N=True if B.current_version!=B.latest_version else False
  G="New ver: "+str(N)
  print(G) 
  return N
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

