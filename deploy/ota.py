import urequests
import os
import gc
import json
A="1.0"
class OTAUpdater:
 def __init__(L,J,r):
  L.filename=r
  L.repo_url=J
  L.version_file=r+'_'+'ver.json'
  L.version_url=L.process_version_url(J,r) 
  L.firmware_url=J+r 
  if L.version_file in os.listdir():
   with open(L.version_file)as f:
    L.current_version=json.load(f)['version']
  else:
   L.current_version="0"
   with open(L.version_file,'w')as f:
    json.dump({'version':L.current_version},f)
 def process_version_url(L,J,r):
  l=J.replace("raw.githubusercontent.com","github.com") 
  l=l.replace("/","§",4) 
  l=l.replace("/","/latest-commit/",1) 
  l=l.replace("§","/",4) 
  l=l+r 
  return l
 def fetch_latest_code(L)->bool:
  k=urequests.get(L.firmware_url,timeout=20)
  if k.status_code==200:
   gc.collect()
   try:
    L.latest_code=k.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif k.status_code==404:
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
  C={"accept":"application/json"}
  k=urequests.get(L.version_url,headers=C,timeout=5)
  m=json.loads(k.text)
  L.latest_version=m['oid'] 
  a=True if L.current_version!=L.latest_version else False
  b="New ver: "+str(a)
  print(b) 
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

