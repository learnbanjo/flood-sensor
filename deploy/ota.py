import urequests
import os
import gc
import json
n="1.0"
class OTAUpdater:
 def __init__(y,B,e):
  y.filename=e
  y.repo_url=B
  y.version_file=e+'_'+'ver.json'
  y.version_url=y.process_version_url(B,e) 
  y.firmware_url=B+e 
  print("Version URL is ",y.version_url)
  print("Firmware URL is ",y.firmware_url)
  if y.version_file in os.listdir():
   with open(y.version_file)as f:
    y.current_version=json.load(f)['version']
   m="Current "+y.filename+" is "+y.current_version
   print("version message ",m)
  else:
   print("No version file")
   y.current_version="0"
   with open(y.version_file,'w')as f:
    json.dump({'version':y.current_version},f)
 def process_version_url(y,B,e):
  i=B.replace("raw.githubusercontent.com","github.com") 
  i=i.replace("/","§",4) 
  i=i.replace("/","/latest-commit/",1) 
  i=i.replace("§","/",4) 
  i=i+e 
  return i
 def fetch_latest_code(y)->bool:
  M=urequests.get(y.firmware_url,timeout=20)
  if M.status_code==200:
   gc.collect()
   try:
    y.latest_code=M.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif M.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(y):
  with open('latest_code.py','w')as f:
   f.write(y.latest_code)
  y.current_version=y.latest_version
  with open(y.version_file,'w')as f:
   json.dump({'version':y.current_version},f)
  y.latest_code=None
  os.rename('latest_code.py',y.filename)
 def check_for_updates(y):
  print('Checking for latest version...')
  gc.collect()
  w={"accept":"application/json"}
  M=urequests.get(y.version_url,headers=w,timeout=5)
  A=json.loads(M.text)
  y.latest_version=A['oid'] 
  l=True if y.current_version!=y.latest_version else False
  Y="New ver: "+str(l)
  print(Y) 
  return l
 def download_and_install_update_if_available(y):
  if y.check_for_updates():
   return y.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(y):
  if y.fetch_latest_code():
   y.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

