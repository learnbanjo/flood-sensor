import urequests
import os
import gc
import json
Q="1.0"
class OTAUpdater:
 def __init__(c,B,g):
  c.filename=g
  c.repo_url=B
  c.version_file=g+'_'+'ver.json'
  c.version_url=c.process_version_url(B,g) 
  c.firmware_url=B+g 
  if c.version_file in os.listdir():
   with open(c.version_file)as f:
    c.current_version=json.load(f)['version']
  else:
   c.current_version="0"
   with open(c.version_file,'w')as f:
    json.dump({'version':c.current_version},f)
 def process_version_url(c,B,g):
  w=B.replace("raw.githubusercontent.com","github.com") 
  w=w.replace("/","§",4) 
  w=w.replace("/","/latest-commit/",1) 
  w=w.replace("§","/",4) 
  w=w+g 
  return w
 def fetch_latest_code(c)->bool:
  u=urequests.get(c.firmware_url,timeout=20)
  if u.status_code==200:
   gc.collect()
   try:
    c.latest_code=u.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif u.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(c):
  with open('latest_code.py','w')as f:
   f.write(c.latest_code)
  c.current_version=c.latest_version
  with open(c.version_file,'w')as f:
   json.dump({'version':c.current_version},f)
  c.latest_code=None
  os.rename('latest_code.py',c.filename)
 def check_for_updates(c):
  gc.collect()
  t={"accept":"application/json"}
  u=urequests.get(c.version_url,headers=t,timeout=5)
  a=json.loads(u.text)
  c.latest_version=a['oid'] 
  O=True if c.current_version!=c.latest_version else False
  F="New ver: "+str(O)
  print(F) 
  return O
 def download_and_install_update_if_available(c):
  if c.check_for_updates():
   return c.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(c):
  if c.fetch_latest_code():
   c.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

