import urequests
import os
import gc
import json
import micropython
P="1.0"
class OTAUpdater:
 def __init__(E,G,b):
  E.filename=b
  E.repo_url=G
  E.version_file=b+'_'+'ver.json'
  E.version_url=E.process_version_url(G,b) 
  E.firmware_url=G+b 
  print("Version URL is ",E.version_url)
  print("Firmware URL is ",E.firmware_url)
  if E.version_file in os.listdir():
   with open(E.version_file)as f:
    E.current_version=json.load(f)['version']
   R="Current "+E.filename+" is "+E.current_version
   print("version message ",R)
  else:
   print("No version file")
   E.current_version="0"
   with open(E.version_file,'w')as f:
    json.dump({'version':E.current_version},f)
 def process_version_url(E,G,b):
  w=G.replace("raw.githubusercontent.com","github.com") 
  w=w.replace("/","§",4) 
  w=w.replace("/","/latest-commit/",1) 
  w=w.replace("§","/",4) 
  w=w+b 
  return w
 def fetch_latest_code(E)->bool:
  j=urequests.get(E.firmware_url,timeout=20)
  if j.status_code==200:
   gc.collect()
   try:
    E.latest_code=j.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif j.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(E):
  with open('latest_code.py','w')as f:
   f.write(E.latest_code)
  E.current_version=E.latest_version
  with open(E.version_file,'w')as f:
   json.dump({'version':E.current_version},f)
  E.latest_code=None
  os.rename('latest_code.py',E.filename)
 def check_for_updates(E):
  print('Checking for latest version...')
  gc.collect()
  e={"accept":"application/json"}
  j=urequests.get(E.version_url,headers=e,timeout=5)
  M=json.loads(j.text)
  E.latest_version=M['oid'] 
  s=True if E.current_version!=E.latest_version else False
  B="New ver: "+str(s)
  print(B) 
  return s
 def download_and_install_update_if_available(E):
  if E.check_for_updates():
   return E.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(E):
  if E.fetch_latest_code():
   E.update_no_reset()
  else:
   return False
  return True

