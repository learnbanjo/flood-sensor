import urequests
import os
import gc
import json
e="1.0"
class OTAUpdater:
 def __init__(g,u,N):
  g.filename=N
  g.repo_url=u
  g.version_file=N+'_'+'ver.json'
  g.version_url=g.process_version_url(u,N) 
  g.firmware_url=u+N 
  print("Version URL is ",g.version_url)
  print("Firmware URL is ",g.firmware_url)
  if g.version_file in os.listdir():
   with open(g.version_file)as f:
    g.current_version=json.load(f)['version']
   a="Current "+g.filename+" is "+g.current_version
   print("version message ",a)
  else:
   print("No version file")
   g.current_version="0"
   with open(g.version_file,'w')as f:
    json.dump({'version':g.current_version},f)
 def process_version_url(g,u,N):
  I=u.replace("raw.githubusercontent.com","github.com") 
  I=I.replace("/","§",4) 
  I=I.replace("/","/latest-commit/",1) 
  I=I.replace("§","/",4) 
  I=I+N 
  return I
 def fetch_latest_code(g)->bool:
  K=urequests.get(g.firmware_url,timeout=20)
  if K.status_code==200:
   gc.collect()
   try:
    g.latest_code=K.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif K.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(g):
  with open('latest_code.py','w')as f:
   f.write(g.latest_code)
  g.current_version=g.latest_version
  with open(g.version_file,'w')as f:
   json.dump({'version':g.current_version},f)
  g.latest_code=None
  os.rename('latest_code.py',g.filename)
 def check_for_updates(g):
  print('Checking for latest version...')
  gc.collect()
  W={"accept":"application/json"}
  K=urequests.get(g.version_url,headers=W,timeout=5)
  S=json.loads(K.text)
  g.latest_version=S['oid'] 
  H=True if g.current_version!=g.latest_version else False
  X="New ver: "+str(H)
  print(X) 
  return H
 def download_and_install_update_if_available(g):
  if g.check_for_updates():
   return g.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(g):
  if g.fetch_latest_code():
   g.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

