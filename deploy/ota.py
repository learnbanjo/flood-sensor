import urequests
import os
import gc
import json
s="1.0"
class OTAUpdater:
 def __init__(t,v,o):
  t.filename=o
  t.repo_url=v
  t.version_file=o+'_'+'ver.json'
  t.version_url=t.process_version_url(v,o) 
  t.firmware_url=v+o 
  print("Version URL is ",t.version_url)
  print("Firmware URL is ",t.firmware_url)
  if t.version_file in os.listdir():
   with open(t.version_file)as f:
    t.current_version=json.load(f)['version']
   P="Current "+t.filename+" is "+t.current_version
   print("version message ",P)
  else:
   print("No version file")
   t.current_version="0"
   with open(t.version_file,'w')as f:
    json.dump({'version':t.current_version},f)
 def process_version_url(t,v,o):
  b=v.replace("raw.githubusercontent.com","github.com") 
  b=b.replace("/","§",4) 
  b=b.replace("/","/latest-commit/",1) 
  b=b.replace("§","/",4) 
  b=b+o 
  return b
 def fetch_latest_code(t)->bool:
  M=urequests.get(t.firmware_url,timeout=20)
  if M.status_code==200:
   gc.collect()
   try:
    t.latest_code=M.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif M.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(t):
  with open('latest_code.py','w')as f:
   f.write(t.latest_code)
  t.current_version=t.latest_version
  with open(t.version_file,'w')as f:
   json.dump({'version':t.current_version},f)
  t.latest_code=None
  os.rename('latest_code.py',t.filename)
 def check_for_updates(t):
  print('Checking for latest version...')
  gc.collect()
  N={"accept":"application/json"}
  M=urequests.get(t.version_url,headers=N,timeout=5)
  K=json.loads(M.text)
  t.latest_version=K['oid'] 
  B=True if t.current_version!=t.latest_version else False
  m="New ver: "+str(B)
  print(m) 
  return B
 def download_and_install_update_if_available(t):
  if t.check_for_updates():
   return t.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(t):
  if t.fetch_latest_code():
   t.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

