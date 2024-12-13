import urequests
import os
import gc
import json
D="1.0"
class OTAUpdater:
 def __init__(O,b,q):
  O.filename=q
  O.repo_url=b
  O.version_file=q+'_'+'ver.json'
  O.version_url=O.process_version_url(b,q) 
  O.firmware_url=b+q 
  if O.version_file in os.listdir():
   with open(O.version_file)as f:
    O.current_version=json.load(f)['version']
  else:
   O.current_version="0"
   with open(O.version_file,'w')as f:
    json.dump({'version':O.current_version},f)
 def process_version_url(O,b,q):
  f=b.replace("raw.githubusercontent.com","github.com") 
  f=f.replace("/","§",4) 
  f=f.replace("/","/latest-commit/",1) 
  f=f.replace("§","/",4) 
  f=f+q 
  return f
 def fetch_latest_code(O)->bool:
  N=urequests.get(O.firmware_url,timeout=20)
  if N.status_code==200:
   gc.collect()
   try:
    O.latest_code=N.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif N.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(O):
  with open('latest_code.py','w')as f:
   f.write(O.latest_code)
  O.current_version=O.latest_version
  with open(O.version_file,'w')as f:
   json.dump({'version':O.current_version},f)
  O.latest_code=None
  os.rename('latest_code.py',O.filename)
 def check_for_updates(O):
  gc.collect()
  T={"accept":"application/json"}
  N=urequests.get(O.version_url,headers=T,timeout=5)
  j=json.loads(N.text)
  O.latest_version=j['oid'] 
  d=True if O.current_version!=O.latest_version else False
  G="New ver: "+str(d)
  print(G) 
  return d
 def download_and_install_update_if_available(O):
  if O.check_for_updates():
   return O.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(O):
  if O.fetch_latest_code():
   O.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

