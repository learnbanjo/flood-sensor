import urequests
import os
import gc
import json
t="1.0"
class OTAUpdater:
 def __init__(A,K,s):
  A.filename=s
  A.repo_url=K
  A.version_file=s+'_'+'ver.json'
  A.version_url=A.process_version_url(K,s) 
  A.firmware_url=K+s 
  print("Version URL is ",A.version_url)
  print("Firmware URL is ",A.firmware_url)
  if A.version_file in os.listdir():
   with open(A.version_file)as f:
    A.current_version=json.load(f)['version']
   b="Current "+A.filename+" is "+A.current_version
   print("version message ",b)
  else:
   print("No version file")
   A.current_version="0"
   with open(A.version_file,'w')as f:
    json.dump({'version':A.current_version},f)
 def process_version_url(A,K,s):
  g=K.replace("raw.githubusercontent.com","github.com") 
  g=g.replace("/","§",4) 
  g=g.replace("/","/latest-commit/",1) 
  g=g.replace("§","/",4) 
  g=g+s 
  return g
 def fetch_latest_code(A)->bool:
  H=urequests.get(A.firmware_url,timeout=20)
  if H.status_code==200:
   gc.collect()
   try:
    A.latest_code=H.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif H.status_code==404:
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
  J={"accept":"application/json"}
  H=urequests.get(A.version_url,headers=J,timeout=5)
  f=json.loads(H.text)
  A.latest_version=f['oid'] 
  I=True if A.current_version!=A.latest_version else False
  R="New ver: "+str(I)
  print(R) 
  return I
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

