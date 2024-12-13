import urequests
import os
import gc
import json
j="1.0"
class OTAUpdater:
 def __init__(A,h,g):
  A.filename=g
  A.repo_url=h
  A.version_file=g+'_'+'ver.json'
  A.version_url=A.process_version_url(h,g) 
  A.firmware_url=h+g 
  if A.version_file in os.listdir():
   with open(A.version_file)as f:
    A.current_version=json.load(f)['version']
  else:
   A.current_version="0"
   with open(A.version_file,'w')as f:
    json.dump({'version':A.current_version},f)
 def process_version_url(A,h,g):
  T=h.replace("raw.githubusercontent.com","github.com") 
  T=T.replace("/","§",4) 
  T=T.replace("/","/latest-commit/",1) 
  T=T.replace("§","/",4) 
  T=T+g 
  return T
 def fetch_latest_code(A)->bool:
  Q=urequests.get(A.firmware_url,timeout=20)
  if Q.status_code==200:
   gc.collect()
   try:
    A.latest_code=Q.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif Q.status_code==404:
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
  gc.collect()
  S={"accept":"application/json"}
  Q=urequests.get(A.version_url,headers=S,timeout=5)
  O=json.loads(Q.text)
  A.latest_version=O['oid'] 
  Y=True if A.current_version!=A.latest_version else False
  N="New ver: "+str(Y)
  print(N) 
  return Y
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

