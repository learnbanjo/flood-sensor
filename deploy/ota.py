import urequests
import os
import gc
import json
h="1.0"
class OTAUpdater:
 def __init__(n,T,f):
  n.filename=f
  n.repo_url=T
  n.version_file=f+'_'+'ver.json'
  n.version_url=n.process_version_url(T,f) 
  n.firmware_url=T+f 
  print("Version URL is ",n.version_url)
  print("Firmware URL is ",n.firmware_url)
  if n.version_file in os.listdir():
   with open(n.version_file)as f:
    n.current_version=json.load(f)['version']
   z="Current "+n.filename+" is "+n.current_version
   print("version message ",z)
  else:
   print("No version file")
   n.current_version="0"
   with open(n.version_file,'w')as f:
    json.dump({'version':n.current_version},f)
 def process_version_url(n,T,f):
  L=T.replace("raw.githubusercontent.com","github.com") 
  L=L.replace("/","§",4) 
  L=L.replace("/","/latest-commit/",1) 
  L=L.replace("§","/",4) 
  L=L+f 
  return L
 def fetch_latest_code(n)->bool:
  U=urequests.get(n.firmware_url,timeout=20)
  if U.status_code==200:
   gc.collect()
   try:
    n.latest_code=U.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif U.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(n):
  with open('latest_code.py','w')as f:
   f.write(n.latest_code)
  n.current_version=n.latest_version
  with open(n.version_file,'w')as f:
   json.dump({'version':n.current_version},f)
  n.latest_code=None
  os.rename('latest_code.py',n.filename)
 def check_for_updates(n):
  print('Checking for latest version...')
  gc.collect()
  q={"accept":"application/json"}
  U=urequests.get(n.version_url,headers=q,timeout=5)
  J=json.loads(U.text)
  n.latest_version=J['oid'] 
  o=True if n.current_version!=n.latest_version else False
  P="New ver: "+str(o)
  print(P) 
  return o
 def download_and_install_update_if_available(n):
  if n.check_for_updates():
   return n.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(n):
  if n.fetch_latest_code():
   n.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

