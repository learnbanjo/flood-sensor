import urequests
import os
import gc
import json
k="1.0"
class OTAUpdater:
 def __init__(p,s,z):
  p.filename=z
  p.repo_url=s
  p.version_file=z+'_'+'ver.json'
  p.version_url=p.process_version_url(s,z) 
  p.firmware_url=s+z 
  print("Version URL is ",p.version_url)
  print("Firmware URL is ",p.firmware_url)
  if p.version_file in os.listdir():
   with open(p.version_file)as f:
    p.current_version=json.load(f)['version']
   J="Current "+p.filename+" is "+p.current_version
   print("version message ",J)
  else:
   print("No version file")
   p.current_version="0"
   with open(p.version_file,'w')as f:
    json.dump({'version':p.current_version},f)
 def process_version_url(p,s,z):
  l=s.replace("raw.githubusercontent.com","github.com") 
  l=l.replace("/","§",4) 
  l=l.replace("/","/latest-commit/",1) 
  l=l.replace("§","/",4) 
  l=l+z 
  return l
 def fetch_latest_code(p)->bool:
  K=urequests.get(p.firmware_url,timeout=20)
  if K.status_code==200:
   gc.collect()
   try:
    p.latest_code=K.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif K.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(p):
  with open('latest_code.py','w')as f:
   f.write(p.latest_code)
  p.current_version=p.latest_version
  with open(p.version_file,'w')as f:
   json.dump({'version':p.current_version},f)
  p.latest_code=None
  os.rename('latest_code.py',p.filename)
 def check_for_updates(p):
  print('Checking for latest version...')
  gc.collect()
  u={"accept":"application/json"}
  K=urequests.get(p.version_url,headers=u,timeout=5)
  X=json.loads(K.text)
  p.latest_version=X['oid'] 
  E=True if p.current_version!=p.latest_version else False
  I="New ver: "+str(E)
  print(I) 
  return E
 def download_and_install_update_if_available(p):
  if p.check_for_updates():
   return p.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(p):
  if p.fetch_latest_code():
   p.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

