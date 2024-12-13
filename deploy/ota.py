import urequests
import os
import gc
import json
J="1.0"
class OTAUpdater:
 def __init__(m,O,B):
  m.filename=B
  m.repo_url=O
  m.version_file=B+'_'+'ver.json'
  m.version_url=m.process_version_url(O,B) 
  m.firmware_url=O+B 
  if m.version_file in os.listdir():
   with open(m.version_file)as f:
    m.current_version=json.load(f)['version']
  else:
   m.current_version="0"
   with open(m.version_file,'w')as f:
    json.dump({'version':m.current_version},f)
 def process_version_url(m,O,B):
  K=O.replace("raw.githubusercontent.com","github.com") 
  K=K.replace("/","§",4) 
  K=K.replace("/","/latest-commit/",1) 
  K=K.replace("§","/",4) 
  K=K+B 
  return K
 def fetch_latest_code(m)->bool:
  y=urequests.get(m.firmware_url,timeout=20)
  if y.status_code==200:
   gc.collect()
   try:
    m.latest_code=y.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif y.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(m):
  with open('latest_code.py','w')as f:
   f.write(m.latest_code)
  m.current_version=m.latest_version
  with open(m.version_file,'w')as f:
   json.dump({'version':m.current_version},f)
  m.latest_code=None
  os.rename('latest_code.py',m.filename)
 def check_for_updates(m):
  gc.collect()
  N={"accept":"application/json"}
  y=urequests.get(m.version_url,headers=N,timeout=5)
  d=json.loads(y.text)
  m.latest_version=d['oid'] 
  l=True if m.current_version!=m.latest_version else False
  A="New ver: "+str(l)
  print(A) 
  return l
 def download_and_install_update_if_available(m):
  if m.check_for_updates():
   return m.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(m):
  if m.fetch_latest_code():
   m.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

