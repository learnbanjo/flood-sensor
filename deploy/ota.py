import urequests
import os
import gc
import json
l="1.0"
class OTAUpdater:
 def __init__(r,H,z):
  r.filename=z
  r.repo_url=H
  r.version_file=z+'_'+'ver.json'
  r.version_url=r.process_version_url(H,z) 
  r.firmware_url=H+z 
  print("Version URL is ",r.version_url)
  print("Firmware URL is ",r.firmware_url)
  if r.version_file in os.listdir():
   with open(r.version_file)as f:
    r.current_version=json.load(f)['version']
   K="Current "+r.filename+" is "+r.current_version
   print("version message ",K)
  else:
   print("No version file")
   r.current_version="0"
   with open(r.version_file,'w')as f:
    json.dump({'version':r.current_version},f)
 def process_version_url(r,H,z):
  h=H.replace("raw.githubusercontent.com","github.com") 
  h=h.replace("/","§",4) 
  h=h.replace("/","/latest-commit/",1) 
  h=h.replace("§","/",4) 
  h=h+z 
  return h
 def fetch_latest_code(r)->bool:
  c=urequests.get(r.firmware_url,timeout=20)
  if c.status_code==200:
   gc.collect()
   try:
    r.latest_code=c.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif c.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(r):
  with open('latest_code.py','w')as f:
   f.write(r.latest_code)
  r.current_version=r.latest_version
  with open(r.version_file,'w')as f:
   json.dump({'version':r.current_version},f)
  r.latest_code=None
  os.rename('latest_code.py',r.filename)
 def check_for_updates(r):
  print('Checking for latest version...')
  gc.collect()
  I={"accept":"application/json"}
  c=urequests.get(r.version_url,headers=I,timeout=5)
  p=json.loads(c.text)
  r.latest_version=p['oid'] 
  J=True if r.current_version!=r.latest_version else False
  k="New ver: "+str(J)
  print(k) 
  return J
 def download_and_install_update_if_available(r):
  if r.check_for_updates():
   return r.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(r):
  if r.fetch_latest_code():
   r.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

