import urequests
import os
import gc
import json
W="1.0"
class OTAUpdater:
 def __init__(A,s,q):
  A.filename=q
  A.repo_url=s
  A.version_file=q+'_'+'ver.json'
  A.version_url=A.process_version_url(s,q) 
  A.firmware_url=s+q 
  print("Version URL is ",A.version_url)
  print("Firmware URL is ",A.firmware_url)
  if A.version_file in os.listdir():
   with open(A.version_file)as f:
    A.current_version=json.load(f)['version']
   U="Current "+A.filename+" is "+A.current_version
   print("version message ",U)
  else:
   print("No version file")
   A.current_version="0"
   with open(A.version_file,'w')as f:
    json.dump({'version':A.current_version},f)
 def process_version_url(A,s,q):
  S=s.replace("raw.githubusercontent.com","github.com") 
  S=S.replace("/","§",4) 
  S=S.replace("/","/latest-commit/",1) 
  S=S.replace("§","/",4) 
  S=S+q 
  return S
 def fetch_latest_code(A)->bool:
  x=urequests.get(A.firmware_url,timeout=20)
  if x.status_code==200:
   gc.collect()
   try:
    A.latest_code=x.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif x.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(A):
  with open('latest_code.py','w')as f:
   f.write(A.latest_code)
  A.current_version=A.latest_version
  with open(A.version_file,'w')as f:
   json.dump({'version':A.current_version},f)
  A.latest_code=None
  os.rename('latest_code.py',A.filename)
 def check_for_updates(A):
  print('Checking for latest version...')
  gc.collect()
  R={"accept":"application/json"}
  x=urequests.get(A.version_url,headers=R,timeout=5)
  D=json.loads(x.text)
  A.latest_version=D['oid'] 
  c=True if A.current_version!=A.latest_version else False
  I="New ver: "+str(c)
  print(I) 
  return c
 def download_and_install_update_if_available(A):
  if A.check_for_updates():
   return A.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(A):
  if A.fetch_latest_code():
   A.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

