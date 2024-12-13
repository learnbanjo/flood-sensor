import urequests
import os
import gc
import json
N="1.0"
class OTAUpdater:
 def __init__(s,X,d):
  s.filename=d
  s.repo_url=X
  s.version_file=d+'_'+'ver.json'
  s.version_url=s.process_version_url(X,d) 
  s.firmware_url=X+d 
  if s.version_file in os.listdir():
   with open(s.version_file)as f:
    s.current_version=json.load(f)['version']
  else:
   s.current_version="0"
   with open(s.version_file,'w')as f:
    json.dump({'version':s.current_version},f)
 def process_version_url(s,X,d):
  K=X.replace("raw.githubusercontent.com","github.com") 
  K=K.replace("/","§",4) 
  K=K.replace("/","/latest-commit/",1) 
  K=K.replace("§","/",4) 
  K=K+d 
  return K
 def fetch_latest_code(s)->bool:
  G=urequests.get(s.firmware_url,timeout=20)
  if G.status_code==200:
   gc.collect()
   try:
    s.latest_code=G.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif G.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(s):
  with open('latest_code.py','w')as f:
   f.write(s.latest_code)
  s.current_version=s.latest_version
  with open(s.version_file,'w')as f:
   json.dump({'version':s.current_version},f)
  s.latest_code=None
  os.rename('latest_code.py',s.filename)
 def check_for_updates(s):
  gc.collect()
  u={"accept":"application/json"}
  G=urequests.get(s.version_url,headers=u,timeout=5)
  L=json.loads(G.text)
  s.latest_version=L['oid'] 
  i=True if s.current_version!=s.latest_version else False
  e="New ver: "+str(i)
  print(e) 
  return i
 def download_and_install_update_if_available(s):
  if s.check_for_updates():
   return s.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(s):
  if s.fetch_latest_code():
   s.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

