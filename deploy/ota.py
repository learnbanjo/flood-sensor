import urequests
import os
import gc
import json
C="1.0"
class OTAUpdater:
 def __init__(L,l,O):
  L.filename=O
  L.repo_url=l
  L.version_file=O+'_'+'ver.json'
  L.version_url=L.process_version_url(l,O) 
  L.firmware_url=l+O 
  if L.version_file in os.listdir():
   with open(L.version_file)as f:
    L.current_version=json.load(f)['version']
  else:
   L.current_version="0"
   with open(L.version_file,'w')as f:
    json.dump({'version':L.current_version},f)
 def process_version_url(L,l,O):
  x=l.replace("raw.githubusercontent.com","github.com") 
  x=x.replace("/","§",4) 
  x=x.replace("/","/latest-commit/",1) 
  x=x.replace("§","/",4) 
  x=x+O 
  return x
 def fetch_latest_code(L)->bool:
  e=urequests.get(L.firmware_url,timeout=20)
  if e.status_code==200:
   gc.collect()
   try:
    L.latest_code=e.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif e.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(L):
  with open('latest_code.py','w')as f:
   f.write(L.latest_code)
  L.current_version=L.latest_version
  with open(L.version_file,'w')as f:
   json.dump({'version':L.current_version},f)
  L.latest_code=None
  os.rename('latest_code.py',L.filename)
 def check_for_updates(L):
  gc.collect()
  u={"accept":"application/json"}
  e=urequests.get(L.version_url,headers=u,timeout=5)
  m=json.loads(e.text)
  L.latest_version=m['oid'] 
  d=True if L.current_version!=L.latest_version else False
  S="New ver: "+str(d)
  print(S) 
  return d
 def download_and_install_update_if_available(L):
  if L.check_for_updates():
   return L.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(L):
  if L.fetch_latest_code():
   L.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

