import urequests
import os
import gc
import json
N="1.0"
class OTAUpdater:
 def __init__(M,G,y):
  M.filename=y
  M.repo_url=G
  M.version_file=y+'_'+'ver.json'
  M.version_url=M.process_version_url(G,y) 
  M.firmware_url=G+y 
  if M.version_file in os.listdir():
   with open(M.version_file)as f:
    M.current_version=json.load(f)['version']
  else:
   M.current_version="0"
   with open(M.version_file,'w')as f:
    json.dump({'version':M.current_version},f)
 def process_version_url(M,G,y):
  z=G.replace("raw.githubusercontent.com","github.com") 
  z=z.replace("/","§",4) 
  z=z.replace("/","/latest-commit/",1) 
  z=z.replace("§","/",4) 
  z=z+y 
  return z
 def fetch_latest_code(M)->bool:
  i=urequests.get(M.firmware_url,timeout=20)
  if i.status_code==200:
   gc.collect()
   try:
    M.latest_code=i.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif i.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(M):
  with open('latest_code.py','w')as f:
   f.write(M.latest_code)
  M.current_version=M.latest_version
  with open(M.version_file,'w')as f:
   json.dump({'version':M.current_version},f)
  M.latest_code=None
  os.rename('latest_code.py',M.filename)
 def check_for_updates(M):
  gc.collect()
  a={"accept":"application/json"}
  i=urequests.get(M.version_url,headers=a,timeout=5)
  I=json.loads(i.text)
  M.latest_version=I['oid'] 
  n=True if M.current_version!=M.latest_version else False
  p="New ver: "+str(n)
  print(p) 
  return n
 def download_and_install_update_if_available(M):
  if M.check_for_updates():
   return M.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(M):
  if M.fetch_latest_code():
   M.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

