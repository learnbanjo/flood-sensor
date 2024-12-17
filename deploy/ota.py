import urequests
import os
import gc
import json
M="1.0"
class OTAUpdater:
 def __init__(q,E,t):
  q.filename=t
  q.repo_url=E
  q.version_file=t+'_'+'ver.json'
  q.version_url=q.process_version_url(E,t) 
  q.firmware_url=E+t 
  print("Version URL is ",q.version_url)
  print("Firmware URL is ",q.firmware_url)
  if q.version_file in os.listdir():
   with open(q.version_file)as f:
    q.current_version=json.load(f)['version']
   I="Current "+q.filename+" is "+q.current_version
   print("version message ",I)
  else:
   print("No version file")
   q.current_version="0"
   with open(q.version_file,'w')as f:
    json.dump({'version':q.current_version},f)
 def process_version_url(q,E,t):
  l=E.replace("raw.githubusercontent.com","github.com") 
  l=l.replace("/","§",4) 
  l=l.replace("/","/latest-commit/",1) 
  l=l.replace("§","/",4) 
  l=l+t 
  return l
 def fetch_latest_code(q)->bool:
  C=urequests.get(q.firmware_url,timeout=20)
  if C.status_code==200:
   gc.collect()
   try:
    q.latest_code=C.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif C.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(q):
  with open('latest_code.py','w')as f:
   f.write(q.latest_code)
  q.current_version=q.latest_version
  with open(q.version_file,'w')as f:
   json.dump({'version':q.current_version},f)
  q.latest_code=None
  os.rename('latest_code.py',q.filename)
 def check_for_updates(q):
  print('Checking for latest version...')
  gc.collect()
  j={"accept":"application/json"}
  C=urequests.get(q.version_url,headers=j,timeout=5)
  a=json.loads(C.text)
  q.latest_version=a['oid'] 
  e=True if q.current_version!=q.latest_version else False
  i="New ver: "+str(e)
  print(i) 
  return e
 def download_and_install_update_if_available(q):
  if q.check_for_updates():
   return q.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(q):
  if q.fetch_latest_code():
   q.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

