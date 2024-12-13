import urequests
import os
import gc
import json
I="1.0"
class OTAUpdater:
 def __init__(w,P,H):
  w.filename=H
  w.repo_url=P
  w.version_file=H+'_'+'ver.json'
  w.version_url=w.process_version_url(P,H) 
  w.firmware_url=P+H 
  if w.version_file in os.listdir():
   with open(w.version_file)as f:
    w.current_version=json.load(f)['version']
  else:
   w.current_version="0"
   with open(w.version_file,'w')as f:
    json.dump({'version':w.current_version},f)
 def process_version_url(w,P,H):
  G=P.replace("raw.githubusercontent.com","github.com") 
  G=G.replace("/","§",4) 
  G=G.replace("/","/latest-commit/",1) 
  G=G.replace("§","/",4) 
  G=G+H 
  return G
 def fetch_latest_code(w)->bool:
  M=urequests.get(w.firmware_url,timeout=20)
  if M.status_code==200:
   gc.collect()
   try:
    w.latest_code=M.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif M.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(w):
  with open('latest_code.py','w')as f:
   f.write(w.latest_code)
  w.current_version=w.latest_version
  with open(w.version_file,'w')as f:
   json.dump({'version':w.current_version},f)
  w.latest_code=None
  os.rename('latest_code.py',w.filename)
 def check_for_updates(w):
  gc.collect()
  F={"accept":"application/json"}
  M=urequests.get(w.version_url,headers=F,timeout=5)
  U=json.loads(M.text)
  w.latest_version=U['oid'] 
  D=True if w.current_version!=w.latest_version else False
  j="New ver: "+str(D)
  print(j) 
  return D
 def download_and_install_update_if_available(w):
  if w.check_for_updates():
   return w.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(w):
  if w.fetch_latest_code():
   w.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

