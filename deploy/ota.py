import urequests
import os
import gc
import json
R="1.0"
class OTAUpdater:
 def __init__(v,l,m):
  v.filename=m
  v.repo_url=l
  v.version_file=m+'_'+'ver.json'
  v.version_url=v.process_version_url(l,m) 
  v.firmware_url=l+m 
  if v.version_file in os.listdir():
   with open(v.version_file)as f:
    v.current_version=json.load(f)['version']
  else:
   v.current_version="0"
   with open(v.version_file,'w')as f:
    json.dump({'version':v.current_version},f)
 def process_version_url(v,l,m):
  g=l.replace("raw.githubusercontent.com","github.com") 
  g=g.replace("/","§",4) 
  g=g.replace("/","/latest-commit/",1) 
  g=g.replace("§","/",4) 
  g=g+m 
  return g
 def fetch_latest_code(v)->bool:
  i=urequests.get(v.firmware_url,timeout=20)
  if i.status_code==200:
   gc.collect()
   try:
    v.latest_code=i.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif i.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(v):
  with open('latest_code.py','w')as f:
   f.write(v.latest_code)
  v.current_version=v.latest_version
  with open(v.version_file,'w')as f:
   json.dump({'version':v.current_version},f)
  v.latest_code=None
  os.rename('latest_code.py',v.filename)
 def check_for_updates(v):
  gc.collect()
  n={"accept":"application/json"}
  i=urequests.get(v.version_url,headers=n,timeout=5)
  H=json.loads(i.text)
  v.latest_version=H['oid'] 
  M=True if v.current_version!=v.latest_version else False
  N="New ver: "+str(M)
  print(N) 
  return M
 def download_and_install_update_if_available(v):
  if v.check_for_updates():
   return v.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(v):
  if v.fetch_latest_code():
   v.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

