import urequests
import os
import gc
import json
N="1.0"
class OTAUpdater:
 def __init__(m,y,D):
  m.filename=D
  m.repo_url=y
  m.version_file=D+'_'+'ver.json'
  m.version_url=m.process_version_url(y,D) 
  m.firmware_url=y+D 
  if m.version_file in os.listdir():
   with open(m.version_file)as f:
    m.current_version=json.load(f)['version']
  else:
   m.current_version="0"
   with open(m.version_file,'w')as f:
    json.dump({'version':m.current_version},f)
 def process_version_url(m,y,D):
  j=y.replace("raw.githubusercontent.com","github.com") 
  j=j.replace("/","§",4) 
  j=j.replace("/","/latest-commit/",1) 
  j=j.replace("§","/",4) 
  j=j+D 
  return j
 def fetch_latest_code(m)->bool:
  t=urequests.get(m.firmware_url,timeout=20)
  if t.status_code==200:
   gc.collect()
   try:
    m.latest_code=t.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif t.status_code==404:
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
  gc.collect()
  S={"accept":"application/json"}
  t=urequests.get(m.version_url,headers=S,timeout=5)
  E=json.loads(t.text)
  m.latest_version=E['oid'] 
  s=True if m.current_version!=m.latest_version else False
  p="New ver: "+str(s)
  print(p) 
  return s
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

