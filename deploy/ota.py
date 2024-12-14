import urequests
import os
import gc
import json
e="1.0"
class OTAUpdater:
 def __init__(P,D,L):
  P.filename=L
  P.repo_url=D
  P.version_file=L+'_'+'ver.json'
  P.version_url=P.process_version_url(D,L) 
  P.firmware_url=D+L 
  if P.version_file in os.listdir():
   with open(P.version_file)as f:
    P.current_version=json.load(f)['version']
  else:
   P.current_version="0"
   with open(P.version_file,'w')as f:
    json.dump({'version':P.current_version},f)
 def process_version_url(P,D,L):
  h=D.replace("raw.githubusercontent.com","github.com") 
  h=h.replace("/","§",4) 
  h=h.replace("/","/latest-commit/",1) 
  h=h.replace("§","/",4) 
  h=h+L 
  return h
 def fetch_latest_code(P)->bool:
  c=urequests.get(P.firmware_url,timeout=20)
  if c.status_code==200:
   gc.collect()
   try:
    P.latest_code=c.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif c.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(P):
  with open('latest_code.py','w')as f:
   f.write(P.latest_code)
  P.current_version=P.latest_version
  with open(P.version_file,'w')as f:
   json.dump({'version':P.current_version},f)
  P.latest_code=None
  os.rename('latest_code.py',P.filename)
 def check_for_updates(P):
  gc.collect()
  o={"accept":"application/json"}
  c=urequests.get(P.version_url,headers=o,timeout=5)
  J=json.loads(c.text)
  P.latest_version=J['oid'] 
  k=True if P.current_version!=P.latest_version else False
  X="New ver: "+str(k)
  print(X) 
  return k
 def download_and_install_update_if_available(P):
  if P.check_for_updates():
   return P.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(P):
  if P.fetch_latest_code():
   P.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

