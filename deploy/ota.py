import urequests
import os
import gc
import json
N="1.0"
class OTAUpdater:
 def __init__(g,U,j):
  g.filename=j
  g.repo_url=U
  g.version_file=j+'_'+'ver.json'
  g.version_url=g.process_version_url(U,j) 
  g.firmware_url=U+j 
  if g.version_file in os.listdir():
   with open(g.version_file)as f:
    g.current_version=json.load(f)['version']
  else:
   g.current_version="0"
   with open(g.version_file,'w')as f:
    json.dump({'version':g.current_version},f)
 def process_version_url(g,U,j):
  D=U.replace("raw.githubusercontent.com","github.com") 
  D=D.replace("/","§",4) 
  D=D.replace("/","/latest-commit/",1) 
  D=D.replace("§","/",4) 
  D=D+j 
  return D
 def fetch_latest_code(g)->bool:
  o=urequests.get(g.firmware_url,timeout=20)
  if o.status_code==200:
   gc.collect()
   try:
    g.latest_code=o.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif o.status_code==404:
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
  c={"accept":"application/json"}
  o=urequests.get(g.version_url,headers=c,timeout=5)
  K=json.loads(o.text)
  g.latest_version=K['oid'] 
  S=True if g.current_version!=g.latest_version else False
  A="New ver: "+str(S)
  print(A) 
  return S
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

