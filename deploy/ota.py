import urequests
import os
import gc
import json
D="1.0"
class OTAUpdater:
 def __init__(B,s,a):
  B.filename=a
  B.repo_url=s
  B.version_file=a+'_'+'ver.json'
  B.version_url=B.process_version_url(s,a) 
  B.firmware_url=s+a 
  if B.version_file in os.listdir():
   with open(B.version_file)as f:
    B.current_version=json.load(f)['version']
  else:
   B.current_version="0"
   with open(B.version_file,'w')as f:
    json.dump({'version':B.current_version},f)
 def process_version_url(B,s,a):
  o=s.replace("raw.githubusercontent.com","github.com") 
  o=o.replace("/","§",4) 
  o=o.replace("/","/latest-commit/",1) 
  o=o.replace("§","/",4) 
  o=o+a 
  return o
 def fetch_latest_code(B)->bool:
  x=urequests.get(B.firmware_url,timeout=20)
  if x.status_code==200:
   gc.collect()
   try:
    B.latest_code=x.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif x.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(B):
  with open('latest_code.py','w')as f:
   f.write(B.latest_code)
  B.current_version=B.latest_version
  with open(B.version_file,'w')as f:
   json.dump({'version':B.current_version},f)
  B.latest_code=None
  os.rename('latest_code.py',B.filename)
 def check_for_updates(B):
  gc.collect()
  I={"accept":"application/json"}
  x=urequests.get(B.version_url,headers=I,timeout=5)
  t=json.loads(x.text)
  B.latest_version=t['oid'] 
  V=True if B.current_version!=B.latest_version else False
  q="New ver: "+str(V)
  print(q) 
  return V
 def download_and_install_update_if_available(B):
  if B.check_for_updates():
   return B.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(B):
  if B.fetch_latest_code():
   B.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

