import urequests
import os
import gc
import json
B="1.0"
class OTAUpdater:
 def __init__(g,K,T):
  g.filename=T
  g.repo_url=K
  g.version_file=T+'_'+'ver.json'
  g.version_url=g.process_version_url(K,T) 
  g.firmware_url=K+T 
  if g.version_file in os.listdir():
   with open(g.version_file)as f:
    g.current_version=json.load(f)['version']
  else:
   g.current_version="0"
   with open(g.version_file,'w')as f:
    json.dump({'version':g.current_version},f)
 def process_version_url(g,K,T):
  C=K.replace("raw.githubusercontent.com","github.com") 
  C=C.replace("/","§",4) 
  C=C.replace("/","/latest-commit/",1) 
  C=C.replace("§","/",4) 
  C=C+T 
  return C
 def fetch_latest_code(g)->bool:
  H=urequests.get(g.firmware_url,timeout=20)
  if H.status_code==200:
   gc.collect()
   try:
    g.latest_code=H.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif H.status_code==404:
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
  gc.collect()
  w={"accept":"application/json"}
  H=urequests.get(g.version_url,headers=w,timeout=5)
  W=json.loads(H.text)
  g.latest_version=W['oid'] 
  F=True if g.current_version!=g.latest_version else False
  y="New ver: "+str(F)
  print(y) 
  return F
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

