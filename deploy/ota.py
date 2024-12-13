import urequests
import os
import gc
import json
w="1.0"
class OTAUpdater:
 def __init__(L,f,t):
  L.filename=t
  L.repo_url=f
  L.version_file=t+'_'+'ver.json'
  L.version_url=L.process_version_url(f,t) 
  L.firmware_url=f+t 
  if L.version_file in os.listdir():
   with open(L.version_file)as f:
    L.current_version=json.load(f)['version']
  else:
   L.current_version="0"
   with open(L.version_file,'w')as f:
    json.dump({'version':L.current_version},f)
 def process_version_url(L,f,t):
  n=f.replace("raw.githubusercontent.com","github.com") 
  n=n.replace("/","§",4) 
  n=n.replace("/","/latest-commit/",1) 
  n=n.replace("§","/",4) 
  n=n+t 
  return n
 def fetch_latest_code(L)->bool:
  i=urequests.get(L.firmware_url,timeout=20)
  if i.status_code==200:
   gc.collect()
   try:
    L.latest_code=i.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif i.status_code==404:
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
  U={"accept":"application/json"}
  i=urequests.get(L.version_url,headers=U,timeout=5)
  S=json.loads(i.text)
  L.latest_version=S['oid'] 
  a=True if L.current_version!=L.latest_version else False
  z="New ver: "+str(a)
  print(z) 
  return a
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

