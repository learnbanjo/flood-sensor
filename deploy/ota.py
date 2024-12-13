import urequests
import os
import gc
import json
g="1.0"
class OTAUpdater:
 def __init__(d,Q,K):
  d.filename=K
  d.repo_url=Q
  d.version_file=K+'_'+'ver.json'
  d.version_url=d.process_version_url(Q,K) 
  d.firmware_url=Q+K 
  if d.version_file in os.listdir():
   with open(d.version_file)as f:
    d.current_version=json.load(f)['version']
  else:
   d.current_version="0"
   with open(d.version_file,'w')as f:
    json.dump({'version':d.current_version},f)
 def process_version_url(d,Q,K):
  b=Q.replace("raw.githubusercontent.com","github.com") 
  b=b.replace("/","§",4) 
  b=b.replace("/","/latest-commit/",1) 
  b=b.replace("§","/",4) 
  b=b+K 
  return b
 def fetch_latest_code(d)->bool:
  P=urequests.get(d.firmware_url,timeout=20)
  if P.status_code==200:
   gc.collect()
   try:
    d.latest_code=P.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif P.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(d):
  with open('latest_code.py','w')as f:
   f.write(d.latest_code)
  d.current_version=d.latest_version
  with open(d.version_file,'w')as f:
   json.dump({'version':d.current_version},f)
  d.latest_code=None
  os.rename('latest_code.py',d.filename)
 def check_for_updates(d):
  gc.collect()
  w={"accept":"application/json"}
  P=urequests.get(d.version_url,headers=w,timeout=5)
  T=json.loads(P.text)
  d.latest_version=T['oid'] 
  I=True if d.current_version!=d.latest_version else False
  R="New ver: "+str(I)
  print(R) 
  return I
 def download_and_install_update_if_available(d):
  if d.check_for_updates():
   return d.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(d):
  if d.fetch_latest_code():
   d.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

