import urequests
import os
import gc
import json
z="1.0"
class OTAUpdater:
 def __init__(p,X,t):
  p.filename=t
  p.repo_url=X
  p.version_file=t+'_'+'ver.json'
  p.version_url=p.process_version_url(X,t) 
  p.firmware_url=X+t 
  print("Version URL is ",p.version_url)
  print("Firmware URL is ",p.firmware_url)
  if p.version_file in os.listdir():
   with open(p.version_file)as f:
    p.current_version=json.load(f)['version']
   l="Current "+p.filename+" is "+p.current_version
   print("version message ",l)
  else:
   print("No version file")
   p.current_version="0"
   with open(p.version_file,'w')as f:
    json.dump({'version':p.current_version},f)
 def process_version_url(p,X,t):
  u=X.replace("raw.githubusercontent.com","github.com") 
  u=u.replace("/","§",4) 
  u=u.replace("/","/latest-commit/",1) 
  u=u.replace("§","/",4) 
  u=u+t 
  return u
 def fetch_latest_code(p)->bool:
  D=urequests.get(p.firmware_url,timeout=20)
  if D.status_code==200:
   gc.collect()
   try:
    p.latest_code=D.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif D.status_code==404:
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
  g={"accept":"application/json"}
  D=urequests.get(p.version_url,headers=g,timeout=5)
  J=json.loads(D.text)
  p.latest_version=J['oid'] 
  G=True if p.current_version!=p.latest_version else False
  H="New ver: "+str(G)
  print(H) 
  return G
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

