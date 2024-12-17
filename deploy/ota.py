import urequests
import os
import gc
import json
u="1.0"
class OTAUpdater:
 def __init__(p,S,i):
  p.filename=i
  p.repo_url=S
  p.version_file=i+'_'+'ver.json'
  p.version_url=p.process_version_url(S,i) 
  p.firmware_url=S+i 
  print("Version URL is ",p.version_url)
  print("Firmware URL is ",p.firmware_url)
  if p.version_file in os.listdir():
   with open(p.version_file)as f:
    p.current_version=json.load(f)['version']
   m="Current "+p.filename+" is "+p.current_version
   print("version message ",m)
  else:
   print("No version file")
   p.current_version="0"
   with open(p.version_file,'w')as f:
    json.dump({'version':p.current_version},f)
 def process_version_url(p,S,i):
  D=S.replace("raw.githubusercontent.com","github.com") 
  D=D.replace("/","§",4) 
  D=D.replace("/","/latest-commit/",1) 
  D=D.replace("§","/",4) 
  D=D+i 
  return D
 def fetch_latest_code(p)->bool:
  x=urequests.get(p.firmware_url,timeout=20)
  if x.status_code==200:
   gc.collect()
   try:
    p.latest_code=x.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif x.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(p):
  with open('latest_code.py','w')as f:
   f.write(p.latest_code)
  p.current_version=p.latest_version
  with open(p.version_file,'w')as f:
   json.dump({'version':p.current_version},f)
  p.latest_code=None
  os.rename('latest_code.py',p.filename)
 def check_for_updates(p):
  print('Checking for latest version...')
  gc.collect()
  w={"accept":"application/json"}
  x=urequests.get(p.version_url,headers=w,timeout=5)
  c=json.loads(x.text)
  p.latest_version=c['oid'] 
  a=True if p.current_version!=p.latest_version else False
  h="New ver: "+str(a)
  print(h) 
  return a
 def download_and_install_update_if_available(p):
  if p.check_for_updates():
   return p.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(p):
  if p.fetch_latest_code():
   p.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

