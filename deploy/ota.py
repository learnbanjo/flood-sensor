import urequests
import os
import gc
import json
Q="1.0"
class OTAUpdater:
 def __init__(h,v,z):
  h.filename=z
  h.repo_url=v
  h.version_file=z+'_'+'ver.json'
  h.version_url=h.process_version_url(v,z) 
  h.firmware_url=v+z 
  print("Version URL is ",h.version_url)
  print("Firmware URL is ",h.firmware_url)
  if h.version_file in os.listdir():
   with open(h.version_file)as f:
    h.current_version=json.load(f)['version']
   P="Current "+h.filename+" is "+h.current_version
   print("version message ",P)
  else:
   print("No version file")
   h.current_version="0"
   with open(h.version_file,'w')as f:
    json.dump({'version':h.current_version},f)
 def process_version_url(h,v,z):
  t=v.replace("raw.githubusercontent.com","github.com") 
  t=t.replace("/","§",4) 
  t=t.replace("/","/latest-commit/",1) 
  t=t.replace("§","/",4) 
  t=t+z 
  return t
 def fetch_latest_code(h)->bool:
  E=urequests.get(h.firmware_url,timeout=20)
  if E.status_code==200:
   gc.collect()
   try:
    h.latest_code=E.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif E.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(h):
  with open('latest_code.py','w')as f:
   f.write(h.latest_code)
  h.current_version=h.latest_version
  with open(h.version_file,'w')as f:
   json.dump({'version':h.current_version},f)
  h.latest_code=None
  os.rename('latest_code.py',h.filename)
 def check_for_updates(h):
  print('Checking for latest version...')
  gc.collect()
  N={"accept":"application/json"}
  E=urequests.get(h.version_url,headers=N,timeout=5)
  m=json.loads(E.text)
  h.latest_version=m['oid'] 
  Y=True if h.current_version!=h.latest_version else False
  U="New ver: "+str(Y)
  print(U) 
  return Y
 def download_and_install_update_if_available(h):
  if h.check_for_updates():
   return h.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(h):
  if h.fetch_latest_code():
   h.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

