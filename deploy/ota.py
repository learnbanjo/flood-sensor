import urequests
import os
import gc
import json
y="1.0"
class OTAUpdater:
 def __init__(c,A,C):
  c.filename=C
  c.repo_url=A
  c.version_file=C+'_'+'ver.json'
  c.version_url=c.process_version_url(A,C) 
  c.firmware_url=A+C 
  print("Version URL is ",c.version_url)
  print("Firmware URL is ",c.firmware_url)
  if c.version_file in os.listdir():
   with open(c.version_file)as f:
    c.current_version=json.load(f)['version']
   x="Current "+c.filename+" is "+c.current_version
   print("version message ",x)
  else:
   print("No version file")
   c.current_version="0"
   with open(c.version_file,'w')as f:
    json.dump({'version':c.current_version},f)
 def process_version_url(c,A,C):
  O=A.replace("raw.githubusercontent.com","github.com") 
  O=O.replace("/","§",4) 
  O=O.replace("/","/latest-commit/",1) 
  O=O.replace("§","/",4) 
  O=O+C 
  return O
 def fetch_latest_code(c)->bool:
  K=urequests.get(c.firmware_url,timeout=20)
  if K.status_code==200:
   gc.collect()
   try:
    c.latest_code=K.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif K.status_code==404:
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
  print('Checking for latest version...')
  gc.collect()
  d={"accept":"application/json"}
  K=urequests.get(c.version_url,headers=d,timeout=5)
  t=json.loads(K.text)
  c.latest_version=t['oid'] 
  I=True if c.current_version!=c.latest_version else False
  G="New ver: "+str(I)
  print(G) 
  return I
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

