import urequests
import os
import gc
import json
F="1.0"
class OTAUpdater:
 def __init__(m,O,n):
  m.filename=n
  m.repo_url=O
  m.version_file=n+'_'+'ver.json'
  m.version_url=m.process_version_url(O,n) 
  m.firmware_url=O+n 
  print("Version URL is ",m.version_url)
  print("Firmware URL is ",m.firmware_url)
  if m.version_file in os.listdir():
   with open(m.version_file)as f:
    m.current_version=json.load(f)['version']
   y="Current "+m.filename+" is "+m.current_version
   print("version message ",y)
  else:
   print("No version file")
   m.current_version="0"
   with open(m.version_file,'w')as f:
    json.dump({'version':m.current_version},f)
 def process_version_url(m,O,n):
  W=O.replace("raw.githubusercontent.com","github.com") 
  W=W.replace("/","§",4) 
  W=W.replace("/","/latest-commit/",1) 
  W=W.replace("§","/",4) 
  W=W+n 
  return W
 def fetch_latest_code(m)->bool:
  P=urequests.get(m.firmware_url,timeout=20)
  if P.status_code==200:
   gc.collect()
   try:
    m.latest_code=P.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif P.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(m):
  with open('latest_code.py','w')as f:
   f.write(m.latest_code)
  m.current_version=m.latest_version
  with open(m.version_file,'w')as f:
   json.dump({'version':m.current_version},f)
  m.latest_code=None
  os.rename('latest_code.py',m.filename)
 def check_for_updates(m):
  print('Checking for latest version...')
  gc.collect()
  o={"accept":"application/json"}
  P=urequests.get(m.version_url,headers=o,timeout=5)
  H=json.loads(P.text)
  m.latest_version=H['oid'] 
  M=True if m.current_version!=m.latest_version else False
  L="New ver: "+str(M)
  print(L) 
  return M
 def download_and_install_update_if_available(m):
  if m.check_for_updates():
   return m.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(m):
  if m.fetch_latest_code():
   m.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

