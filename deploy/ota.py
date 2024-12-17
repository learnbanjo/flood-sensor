import urequests
import os
import gc
import json
h="1.0"
class OTAUpdater:
 def __init__(L,g,a):
  L.filename=a
  L.repo_url=g
  L.version_file=a+'_'+'ver.json'
  L.version_url=L.process_version_url(g,a) 
  L.firmware_url=g+a 
  print("Version URL is ",L.version_url)
  print("Firmware URL is ",L.firmware_url)
  if L.version_file in os.listdir():
   with open(L.version_file)as f:
    L.current_version=json.load(f)['version']
   d="Current "+L.filename+" is "+L.current_version
   print("version message ",d)
  else:
   print("No version file")
   L.current_version="0"
   with open(L.version_file,'w')as f:
    json.dump({'version':L.current_version},f)
 def process_version_url(L,g,a):
  U=g.replace("raw.githubusercontent.com","github.com") 
  U=U.replace("/","§",4) 
  U=U.replace("/","/latest-commit/",1) 
  U=U.replace("§","/",4) 
  U=U+a 
  return U
 def fetch_latest_code(L)->bool:
  i=urequests.get(L.firmware_url,timeout=20)
  if i.status_code==200:
   gc.collect()
   try:
    L.latest_code=i.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif i.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(L):
  with open('latest_code.py','w')as f:
   f.write(L.latest_code)
  L.current_version=L.latest_version
  with open(L.version_file,'w')as f:
   json.dump({'version':L.current_version},f)
  L.latest_code=None
  os.rename('latest_code.py',L.filename)
 def check_for_updates(L):
  print('Checking for latest version...')
  gc.collect()
  K={"accept":"application/json"}
  i=urequests.get(L.version_url,headers=K,timeout=5)
  C=json.loads(i.text)
  L.latest_version=C['oid'] 
  m=True if L.current_version!=L.latest_version else False
  o="New ver: "+str(m)
  print(o) 
  return m
 def download_and_install_update_if_available(L):
  if L.check_for_updates():
   return L.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(L):
  if L.fetch_latest_code():
   L.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

