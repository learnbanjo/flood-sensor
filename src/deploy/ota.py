import urequests
import os
import gc
import json
import micropython
K="1.0"
class OTAUpdater:
 def __init__(J,A,e):
  J.filename=e
  J.repo_url=A
  J.version_file=e+'_'+'ver.json'
  J.version_url=J.process_version_url(A,e) 
  J.firmware_url=A+e 
  print("Version URL is ",J.version_url)
  print("Firmware URL is ",J.firmware_url)
  if J.version_file in os.listdir():
   with open(J.version_file)as f:
    J.current_version=json.load(f)['version']
   i="Current "+J.filename+" is "+J.current_version
   print("version message ",i)
  else:
   print("No version file")
   J.current_version="0"
   with open(J.version_file,'w')as f:
    json.dump({'version':J.current_version},f)
 def process_version_url(J,A,e):
  s=A.replace("raw.githubusercontent.com","github.com") 
  s=s.replace("/","§",4) 
  s=s.replace("/","/latest-commit/",1) 
  s=s.replace("§","/",4) 
  s=s+e 
  return s
 def fetch_latest_code(J)->bool:
  f=urequests.get(J.firmware_url,timeout=20)
  if f.status_code==200:
   gc.collect()
   try:
    J.latest_code=f.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif f.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(J):
  with open('latest_code.py','w')as f:
   f.write(J.latest_code)
  J.current_version=J.latest_version
  with open(J.version_file,'w')as f:
   json.dump({'version':J.current_version},f)
  J.latest_code=None
  os.rename('latest_code.py',J.filename)
 def check_for_updates(J):
  print('Checking for latest version...')
  gc.collect()
  t={"accept":"application/json"}
  f=urequests.get(J.version_url,headers=t,timeout=5)
  M=json.loads(f.text)
  J.latest_version=M['oid'] 
  E=True if J.current_version!=J.latest_version else False
  I="New ver: "+str(E)
  print(I) 
  return E
 def download_and_install_update_if_available(J):
  if J.check_for_updates():
   return J.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(J):
  if J.fetch_latest_code():
   J.update_no_reset()
  else:
   return False
  return True

