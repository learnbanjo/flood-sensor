import urequests
import os
import gc
import json
J="1.0"
class OTAUpdater:
 def __init__(A,s,h):
  A.filename=h
  A.repo_url=s
  A.version_file=h+'_'+'ver.json'
  A.version_url=A.process_version_url(s,h) 
  A.firmware_url=s+h 
  if A.version_file in os.listdir():
   with open(A.version_file)as f:
    A.current_version=json.load(f)['version']
  else:
   A.current_version="0"
   with open(A.version_file,'w')as f:
    json.dump({'version':A.current_version},f)
 def process_version_url(A,s,h):
  G=s.replace("raw.githubusercontent.com","github.com") 
  G=G.replace("/","§",4) 
  G=G.replace("/","/latest-commit/",1) 
  G=G.replace("§","/",4) 
  G=G+h 
  return G
 def fetch_latest_code(A)->bool:
  V=urequests.get(A.firmware_url,timeout=20)
  if V.status_code==200:
   gc.collect()
   try:
    A.latest_code=V.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif V.status_code==404:
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
  N={"accept":"application/json"}
  V=urequests.get(A.version_url,headers=N,timeout=5)
  H=json.loads(V.text)
  A.latest_version=H['oid'] 
  o=True if A.current_version!=A.latest_version else False
  T="New ver: "+str(o)
  print(T) 
  return o
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

