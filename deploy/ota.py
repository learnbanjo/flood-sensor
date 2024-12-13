import urequests
import os
import gc
import json
U="1.0"
class OTAUpdater:
 def __init__(d,v,l):
  d.filename=l
  d.repo_url=v
  d.version_file=l+'_'+'ver.json'
  d.version_url=d.process_version_url(v,l) 
  d.firmware_url=v+l 
  if d.version_file in os.listdir():
   with open(d.version_file)as f:
    d.current_version=json.load(f)['version']
  else:
   d.current_version="0"
   with open(d.version_file,'w')as f:
    json.dump({'version':d.current_version},f)
 def process_version_url(d,v,l):
  Q=v.replace("raw.githubusercontent.com","github.com") 
  Q=Q.replace("/","§",4) 
  Q=Q.replace("/","/latest-commit/",1) 
  Q=Q.replace("§","/",4) 
  Q=Q+l 
  return Q
 def fetch_latest_code(d)->bool:
  e=urequests.get(d.firmware_url,timeout=20)
  if e.status_code==200:
   gc.collect()
   try:
    d.latest_code=e.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif e.status_code==404:
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
  R={"accept":"application/json"}
  e=urequests.get(d.version_url,headers=R,timeout=5)
  V=json.loads(e.text)
  d.latest_version=V['oid'] 
  F=True if d.current_version!=d.latest_version else False
  H="New ver: "+str(F)
  print(H) 
  return F
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

