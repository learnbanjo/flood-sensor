import urequests
import os
import gc
import json
z="1.0"
class OTAUpdater:
 def __init__(h,x,S):
  h.filename=S
  h.repo_url=x
  h.version_file=S+'_'+'ver.json'
  h.version_url=h.process_version_url(x,S) 
  h.firmware_url=x+S 
  if h.version_file in os.listdir():
   with open(h.version_file)as f:
    h.current_version=json.load(f)['version']
  else:
   h.current_version="0"
   with open(h.version_file,'w')as f:
    json.dump({'version':h.current_version},f)
 def process_version_url(h,x,S):
  M=x.replace("raw.githubusercontent.com","github.com") 
  M=M.replace("/","§",4) 
  M=M.replace("/","/latest-commit/",1) 
  M=M.replace("§","/",4) 
  M=M+S 
  return M
 def fetch_latest_code(h)->bool:
  q=urequests.get(h.firmware_url,timeout=20)
  if q.status_code==200:
   gc.collect()
   try:
    h.latest_code=q.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif q.status_code==404:
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
  gc.collect()
  p={"accept":"application/json"}
  q=urequests.get(h.version_url,headers=p,timeout=5)
  T=json.loads(q.text)
  h.latest_version=T['oid'] 
  e=True if h.current_version!=h.latest_version else False
  w="New ver: "+str(e)
  print(w) 
  return e
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

