import urequests
import os
import gc
import json
j="1.0"
class OTAUpdater:
 def __init__(v,z,u):
  v.filename=u
  v.repo_url=z
  v.version_file=u+'_'+'ver.json'
  v.version_url=v.process_version_url(z,u) 
  v.firmware_url=z+u 
  if v.version_file in os.listdir():
   with open(v.version_file)as f:
    v.current_version=json.load(f)['version']
  else:
   v.current_version="0"
   with open(v.version_file,'w')as f:
    json.dump({'version':v.current_version},f)
 def process_version_url(v,z,u):
  L=z.replace("raw.githubusercontent.com","github.com") 
  L=L.replace("/","§",4) 
  L=L.replace("/","/latest-commit/",1) 
  L=L.replace("§","/",4) 
  L=L+u 
  return L
 def fetch_latest_code(v)->bool:
  h=urequests.get(v.firmware_url,timeout=20)
  if h.status_code==200:
   gc.collect()
   try:
    v.latest_code=h.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif h.status_code==404:
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
  p={"accept":"application/json"}
  h=urequests.get(v.version_url,headers=p,timeout=5)
  e=json.loads(h.text)
  v.latest_version=e['oid'] 
  g=True if v.current_version!=v.latest_version else False
  G="New ver: "+str(g)
  print(G) 
  return g
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

