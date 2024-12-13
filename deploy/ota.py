import urequests
import os
import gc
import json
T="1.0"
class OTAUpdater:
 def __init__(Q,a,G):
  Q.filename=G
  Q.repo_url=a
  Q.version_file=G+'_'+'ver.json'
  Q.version_url=Q.process_version_url(a,G) 
  Q.firmware_url=a+G 
  if Q.version_file in os.listdir():
   with open(Q.version_file)as f:
    Q.current_version=json.load(f)['version']
  else:
   Q.current_version="0"
   with open(Q.version_file,'w')as f:
    json.dump({'version':Q.current_version},f)
 def process_version_url(Q,a,G):
  y=a.replace("raw.githubusercontent.com","github.com") 
  y=y.replace("/","§",4) 
  y=y.replace("/","/latest-commit/",1) 
  y=y.replace("§","/",4) 
  y=y+G 
  return y
 def fetch_latest_code(Q)->bool:
  n=urequests.get(Q.firmware_url,timeout=20)
  if n.status_code==200:
   gc.collect()
   try:
    Q.latest_code=n.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif n.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(Q):
  with open('latest_code.py','w')as f:
   f.write(Q.latest_code)
  Q.current_version=Q.latest_version
  with open(Q.version_file,'w')as f:
   json.dump({'version':Q.current_version},f)
  Q.latest_code=None
  os.rename('latest_code.py',Q.filename)
 def check_for_updates(Q):
  gc.collect()
  u={"accept":"application/json"}
  n=urequests.get(Q.version_url,headers=u,timeout=5)
  D=json.loads(n.text)
  Q.latest_version=D['oid'] 
  C=True if Q.current_version!=Q.latest_version else False
  i="New ver: "+str(C)
  print(i) 
  return C
 def download_and_install_update_if_available(Q):
  if Q.check_for_updates():
   return Q.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(Q):
  if Q.fetch_latest_code():
   Q.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

