import urequests
import os
import gc
import json
z="1.0"
class OTAUpdater:
 def __init__(m,E,D):
  m.filename=D
  m.repo_url=E
  m.version_file=D+'_'+'ver.json'
  m.version_url=m.process_version_url(E,D) 
  m.firmware_url=E+D 
  print("Version URL is ",m.version_url)
  print("Firmware URL is ",m.firmware_url)
  if m.version_file in os.listdir():
   with open(m.version_file)as f:
    m.current_version=json.load(f)['version']
   a="Current "+m.filename+" is "+m.current_version
   print("version message ",a)
  else:
   print("No version file")
   m.current_version="0"
   with open(m.version_file,'w')as f:
    json.dump({'version':m.current_version},f)
 def process_version_url(m,E,D):
  d=E.replace("raw.githubusercontent.com","github.com") 
  d=d.replace("/","§",4) 
  d=d.replace("/","/latest-commit/",1) 
  d=d.replace("§","/",4) 
  d=d+D 
  return d
 def fetch_latest_code(m)->bool:
  X=urequests.get(m.firmware_url,timeout=20)
  if X.status_code==200:
   gc.collect()
   try:
    m.latest_code=X.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif X.status_code==404:
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
  R={"accept":"application/json"}
  X=urequests.get(m.version_url,headers=R,timeout=5)
  p=json.loads(X.text)
  m.latest_version=p['oid'] 
  v=True if m.current_version!=m.latest_version else False
  g="New ver: "+str(v)
  print(g) 
  return v
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

