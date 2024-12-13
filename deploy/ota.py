import urequests
import os
import gc
import json
J="1.0"
class OTAUpdater:
 def __init__(S,l,U):
  S.filename=U
  S.repo_url=l
  S.version_file=U+'_'+'ver.json'
  S.version_url=S.process_version_url(l,U) 
  S.firmware_url=l+U 
  if S.version_file in os.listdir():
   with open(S.version_file)as f:
    S.current_version=json.load(f)['version']
  else:
   S.current_version="0"
   with open(S.version_file,'w')as f:
    json.dump({'version':S.current_version},f)
 def process_version_url(S,l,U):
  G=l.replace("raw.githubusercontent.com","github.com") 
  G=G.replace("/","§",4) 
  G=G.replace("/","/latest-commit/",1) 
  G=G.replace("§","/",4) 
  G=G+U 
  return G
 def fetch_latest_code(S)->bool:
  y=urequests.get(S.firmware_url,timeout=20)
  if y.status_code==200:
   gc.collect()
   try:
    S.latest_code=y.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif y.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(S):
  with open('latest_code.py','w')as f:
   f.write(S.latest_code)
  S.current_version=S.latest_version
  with open(S.version_file,'w')as f:
   json.dump({'version':S.current_version},f)
  S.latest_code=None
  os.rename('latest_code.py',S.filename)
 def check_for_updates(S):
  gc.collect()
  R={"accept":"application/json"}
  y=urequests.get(S.version_url,headers=R,timeout=5)
  n=json.loads(y.text)
  S.latest_version=n['oid'] 
  v=True if S.current_version!=S.latest_version else False
  j="New ver: "+str(v)
  print(j) 
  return v
 def download_and_install_update_if_available(S):
  if S.check_for_updates():
   return S.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(S):
  if S.fetch_latest_code():
   S.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

