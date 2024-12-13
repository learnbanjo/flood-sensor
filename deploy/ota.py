import urequests
import os
import gc
import json
d="1.0"
class OTAUpdater:
 def __init__(k,J,U):
  k.filename=U
  k.repo_url=J
  k.version_file=U+'_'+'ver.json'
  k.version_url=k.process_version_url(J,U) 
  k.firmware_url=J+U 
  if k.version_file in os.listdir():
   with open(k.version_file)as f:
    k.current_version=json.load(f)['version']
  else:
   k.current_version="0"
   with open(k.version_file,'w')as f:
    json.dump({'version':k.current_version},f)
 def process_version_url(k,J,U):
  Q=J.replace("raw.githubusercontent.com","github.com") 
  Q=Q.replace("/","§",4) 
  Q=Q.replace("/","/latest-commit/",1) 
  Q=Q.replace("§","/",4) 
  Q=Q+U 
  return Q
 def fetch_latest_code(k)->bool:
  q=urequests.get(k.firmware_url,timeout=20)
  if q.status_code==200:
   gc.collect()
   try:
    k.latest_code=q.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif q.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(k):
  with open('latest_code.py','w')as f:
   f.write(k.latest_code)
  k.current_version=k.latest_version
  with open(k.version_file,'w')as f:
   json.dump({'version':k.current_version},f)
  k.latest_code=None
  os.rename('latest_code.py',k.filename)
 def check_for_updates(k):
  gc.collect()
  i={"accept":"application/json"}
  q=urequests.get(k.version_url,headers=i,timeout=5)
  m=json.loads(q.text)
  k.latest_version=m['oid'] 
  D=True if k.current_version!=k.latest_version else False
  h="New ver: "+str(D)
  print(h) 
  return D
 def download_and_install_update_if_available(k):
  if k.check_for_updates():
   return k.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(k):
  if k.fetch_latest_code():
   k.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

