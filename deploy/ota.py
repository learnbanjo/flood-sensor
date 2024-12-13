import urequests
import os
import gc
import json
K="1.0"
class OTAUpdater:
 def __init__(U,R,h):
  U.filename=h
  U.repo_url=R
  U.version_file=h+'_'+'ver.json'
  U.version_url=U.process_version_url(R,h) 
  U.firmware_url=R+h 
  if U.version_file in os.listdir():
   with open(U.version_file)as f:
    U.current_version=json.load(f)['version']
  else:
   U.current_version="0"
   with open(U.version_file,'w')as f:
    json.dump({'version':U.current_version},f)
 def process_version_url(U,R,h):
  s=R.replace("raw.githubusercontent.com","github.com") 
  s=s.replace("/","§",4) 
  s=s.replace("/","/latest-commit/",1) 
  s=s.replace("§","/",4) 
  s=s+h 
  return s
 def fetch_latest_code(U)->bool:
  t=urequests.get(U.firmware_url,timeout=20)
  if t.status_code==200:
   gc.collect()
   try:
    U.latest_code=t.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif t.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(U):
  with open('latest_code.py','w')as f:
   f.write(U.latest_code)
  U.current_version=U.latest_version
  with open(U.version_file,'w')as f:
   json.dump({'version':U.current_version},f)
  U.latest_code=None
  os.rename('latest_code.py',U.filename)
 def check_for_updates(U):
  gc.collect()
  P={"accept":"application/json"}
  t=urequests.get(U.version_url,headers=P,timeout=5)
  r=json.loads(t.text)
  U.latest_version=r['oid'] 
  b=True if U.current_version!=U.latest_version else False
  a="New ver: "+str(b)
  print(a) 
  return b
 def download_and_install_update_if_available(U):
  if U.check_for_updates():
   return U.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(U):
  if U.fetch_latest_code():
   U.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

