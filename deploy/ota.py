import urequests
import os
import gc
import json
B="1.0"
class OTAUpdater:
 def __init__(l,M,W):
  l.filename=W
  l.repo_url=M
  l.version_file=W+'_'+'ver.json'
  l.version_url=l.process_version_url(M,W) 
  l.firmware_url=M+W 
  if l.version_file in os.listdir():
   with open(l.version_file)as f:
    l.current_version=json.load(f)['version']
  else:
   l.current_version="0"
   with open(l.version_file,'w')as f:
    json.dump({'version':l.current_version},f)
 def process_version_url(l,M,W):
  L=M.replace("raw.githubusercontent.com","github.com") 
  L=L.replace("/","§",4) 
  L=L.replace("/","/latest-commit/",1) 
  L=L.replace("§","/",4) 
  L=L+W 
  return L
 def fetch_latest_code(l)->bool:
  k=urequests.get(l.firmware_url,timeout=20)
  if k.status_code==200:
   gc.collect()
   try:
    l.latest_code=k.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif k.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(l):
  with open('latest_code.py','w')as f:
   f.write(l.latest_code)
  l.current_version=l.latest_version
  with open(l.version_file,'w')as f:
   json.dump({'version':l.current_version},f)
  l.latest_code=None
  os.rename('latest_code.py',l.filename)
 def check_for_updates(l):
  gc.collect()
  V={"accept":"application/json"}
  k=urequests.get(l.version_url,headers=V,timeout=5)
  i=json.loads(k.text)
  l.latest_version=i['oid'] 
  O=True if l.current_version!=l.latest_version else False
  A="New ver: "+str(O)
  print(A) 
  return O
 def download_and_install_update_if_available(l):
  if l.check_for_updates():
   return l.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(l):
  if l.fetch_latest_code():
   l.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

