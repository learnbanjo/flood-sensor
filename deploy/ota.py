import urequests
import os
import gc
import json
J="1.0"
class OTAUpdater:
 def __init__(i,y,u):
  i.filename=u
  i.repo_url=y
  i.version_file=u+'_'+'ver.json'
  i.version_url=i.process_version_url(y,u) 
  i.firmware_url=y+u 
  print("Version URL is ",i.version_url)
  print("Firmware URL is ",i.firmware_url)
  if i.version_file in os.listdir():
   with open(i.version_file)as f:
    i.current_version=json.load(f)['version']
   s="Current "+i.filename+" is "+i.current_version
   print("version message ",s)
  else:
   print("No version file")
   i.current_version="0"
   with open(i.version_file,'w')as f:
    json.dump({'version':i.current_version},f)
 def process_version_url(i,y,u):
  X=y.replace("raw.githubusercontent.com","github.com") 
  X=X.replace("/","§",4) 
  X=X.replace("/","/latest-commit/",1) 
  X=X.replace("§","/",4) 
  X=X+u 
  return X
 def fetch_latest_code(i)->bool:
  g=urequests.get(i.firmware_url,timeout=20)
  if g.status_code==200:
   gc.collect()
   try:
    i.latest_code=g.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif g.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(i):
  with open('latest_code.py','w')as f:
   f.write(i.latest_code)
  i.current_version=i.latest_version
  with open(i.version_file,'w')as f:
   json.dump({'version':i.current_version},f)
  i.latest_code=None
  os.rename('latest_code.py',i.filename)
 def check_for_updates(i):
  print('Checking for latest version...')
  gc.collect()
  q={"accept":"application/json"}
  g=urequests.get(i.version_url,headers=q,timeout=5)
  Q=json.loads(g.text)
  i.latest_version=Q['oid'] 
  N=True if i.current_version!=i.latest_version else False
  C="New ver: "+str(N)
  print(C) 
  return N
 def download_and_install_update_if_available(i):
  if i.check_for_updates():
   return i.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(i):
  if i.fetch_latest_code():
   i.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

