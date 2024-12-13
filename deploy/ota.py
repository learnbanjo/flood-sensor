import urequests
import os
import gc
import json
o="1.0"
class OTAUpdater:
 def __init__(y,O,G):
  y.filename=G
  y.repo_url=O
  y.version_file=G+'_'+'ver.json'
  y.version_url=y.process_version_url(O,G) 
  y.firmware_url=O+G 
  if y.version_file in os.listdir():
   with open(y.version_file)as f:
    y.current_version=json.load(f)['version']
  else:
   y.current_version="0"
   with open(y.version_file,'w')as f:
    json.dump({'version':y.current_version},f)
 def process_version_url(y,O,G):
  L=O.replace("raw.githubusercontent.com","github.com") 
  L=L.replace("/","§",4) 
  L=L.replace("/","/latest-commit/",1) 
  L=L.replace("§","/",4) 
  L=L+G 
  return L
 def fetch_latest_code(y)->bool:
  H=urequests.get(y.firmware_url,timeout=20)
  if H.status_code==200:
   gc.collect()
   try:
    y.latest_code=H.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif H.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(y):
  with open('latest_code.py','w')as f:
   f.write(y.latest_code)
  y.current_version=y.latest_version
  with open(y.version_file,'w')as f:
   json.dump({'version':y.current_version},f)
  y.latest_code=None
  os.rename('latest_code.py',y.filename)
 def check_for_updates(y):
  gc.collect()
  R={"accept":"application/json"}
  H=urequests.get(y.version_url,headers=R,timeout=5)
  D=json.loads(H.text)
  y.latest_version=D['oid'] 
  n=True if y.current_version!=y.latest_version else False
  S="New ver: "+str(n)
  print(S) 
  return n
 def download_and_install_update_if_available(y):
  if y.check_for_updates():
   return y.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(y):
  if y.fetch_latest_code():
   y.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

