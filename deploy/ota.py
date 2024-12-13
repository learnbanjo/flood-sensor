import urequests
import os
import gc
import json
u="1.0"
class OTAUpdater:
 def __init__(s,x,P):
  s.filename=P
  s.repo_url=x
  s.version_file=P+'_'+'ver.json'
  s.version_url=s.process_version_url(x,P) 
  s.firmware_url=x+P 
  if s.version_file in os.listdir():
   with open(s.version_file)as f:
    s.current_version=json.load(f)['version']
  else:
   s.current_version="0"
   with open(s.version_file,'w')as f:
    json.dump({'version':s.current_version},f)
 def process_version_url(s,x,P):
  M=x.replace("raw.githubusercontent.com","github.com") 
  M=M.replace("/","§",4) 
  M=M.replace("/","/latest-commit/",1) 
  M=M.replace("§","/",4) 
  M=M+P 
  return M
 def fetch_latest_code(s)->bool:
  T=urequests.get(s.firmware_url,timeout=20)
  if T.status_code==200:
   gc.collect()
   try:
    s.latest_code=T.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif T.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(s):
  with open('latest_code.py','w')as f:
   f.write(s.latest_code)
  s.current_version=s.latest_version
  with open(s.version_file,'w')as f:
   json.dump({'version':s.current_version},f)
  s.latest_code=None
  os.rename('latest_code.py',s.filename)
 def check_for_updates(s):
  gc.collect()
  y={"accept":"application/json"}
  T=urequests.get(s.version_url,headers=y,timeout=5)
  B=json.loads(T.text)
  s.latest_version=B['oid'] 
  L=True if s.current_version!=s.latest_version else False
  D="New ver: "+str(L)
  print(D) 
  return L
 def download_and_install_update_if_available(s):
  if s.check_for_updates():
   return s.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(s):
  if s.fetch_latest_code():
   s.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

