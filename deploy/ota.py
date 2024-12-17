import urequests
import os
import gc
import json
P="1.0"
class OTAUpdater:
 def __init__(e,j,G):
  e.filename=G
  e.repo_url=j
  e.version_file=G+'_'+'ver.json'
  e.version_url=e.process_version_url(j,G) 
  e.firmware_url=j+G 
  print("Version URL is ",e.version_url)
  print("Firmware URL is ",e.firmware_url)
  if e.version_file in os.listdir():
   with open(e.version_file)as f:
    e.current_version=json.load(f)['version']
   J="Current "+e.filename+" is "+e.current_version
   print("version message ",J)
  else:
   print("No version file")
   e.current_version="0"
   with open(e.version_file,'w')as f:
    json.dump({'version':e.current_version},f)
 def process_version_url(e,j,G):
  T=j.replace("raw.githubusercontent.com","github.com") 
  T=T.replace("/","§",4) 
  T=T.replace("/","/latest-commit/",1) 
  T=T.replace("§","/",4) 
  T=T+G 
  return T
 def fetch_latest_code(e)->bool:
  l=urequests.get(e.firmware_url,timeout=20)
  if l.status_code==200:
   gc.collect()
   try:
    e.latest_code=l.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif l.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(e):
  with open('latest_code.py','w')as f:
   f.write(e.latest_code)
  e.current_version=e.latest_version
  with open(e.version_file,'w')as f:
   json.dump({'version':e.current_version},f)
  e.latest_code=None
  os.rename('latest_code.py',e.filename)
 def check_for_updates(e):
  print('Checking for latest version...')
  gc.collect()
  F={"accept":"application/json"}
  l=urequests.get(e.version_url,headers=F,timeout=5)
  s=json.loads(l.text)
  e.latest_version=s['oid'] 
  p=True if e.current_version!=e.latest_version else False
  I="New ver: "+str(p)
  print(I) 
  return p
 def download_and_install_update_if_available(e):
  if e.check_for_updates():
   return e.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(e):
  if e.fetch_latest_code():
   e.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

