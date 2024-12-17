import urequests
import os
import gc
import json
e="1.0"
class OTAUpdater:
 def __init__(j,x,Y):
  j.filename=Y
  j.repo_url=x
  j.version_file=Y+'_'+'ver.json'
  j.version_url=j.process_version_url(x,Y) 
  j.firmware_url=x+Y 
  print("Version URL is ",j.version_url)
  print("Firmware URL is ",j.firmware_url)
  if j.version_file in os.listdir():
   with open(j.version_file)as f:
    j.current_version=json.load(f)['version']
   F="Current "+j.filename+" is "+j.current_version
   print("version message ",F)
  else:
   print("No version file")
   j.current_version="0"
   with open(j.version_file,'w')as f:
    json.dump({'version':j.current_version},f)
 def process_version_url(j,x,Y):
  D=x.replace("raw.githubusercontent.com","github.com") 
  D=D.replace("/","§",4) 
  D=D.replace("/","/latest-commit/",1) 
  D=D.replace("§","/",4) 
  D=D+Y 
  return D
 def fetch_latest_code(j)->bool:
  l=urequests.get(j.firmware_url,timeout=20)
  if l.status_code==200:
   gc.collect()
   try:
    j.latest_code=l.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif l.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(j):
  with open('latest_code.py','w')as f:
   f.write(j.latest_code)
  j.current_version=j.latest_version
  with open(j.version_file,'w')as f:
   json.dump({'version':j.current_version},f)
  j.latest_code=None
  os.rename('latest_code.py',j.filename)
 def check_for_updates(j):
  print('Checking for latest version...')
  gc.collect()
  h={"accept":"application/json"}
  l=urequests.get(j.version_url,headers=h,timeout=5)
  d=json.loads(l.text)
  j.latest_version=d['oid'] 
  Q=True if j.current_version!=j.latest_version else False
  A="New ver: "+str(Q)
  print(A) 
  return Q
 def download_and_install_update_if_available(j):
  if j.check_for_updates():
   return j.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(j):
  if j.fetch_latest_code():
   j.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

