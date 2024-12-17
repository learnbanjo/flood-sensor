import urequests
import os
import gc
import json
r="1.0"
class OTAUpdater:
 def __init__(g,Q,U):
  g.filename=U
  g.repo_url=Q
  g.version_file=U+'_'+'ver.json'
  g.version_url=g.process_version_url(Q,U) 
  g.firmware_url=Q+U 
  print("Version URL is ",g.version_url)
  print("Firmware URL is ",g.firmware_url)
  if g.version_file in os.listdir():
   with open(g.version_file)as f:
    g.current_version=json.load(f)['version']
   D="Current "+g.filename+" is "+g.current_version
   print("version message ",D)
  else:
   print("No version file")
   g.current_version="0"
   with open(g.version_file,'w')as f:
    json.dump({'version':g.current_version},f)
 def process_version_url(g,Q,U):
  S=Q.replace("raw.githubusercontent.com","github.com") 
  S=S.replace("/","§",4) 
  S=S.replace("/","/latest-commit/",1) 
  S=S.replace("§","/",4) 
  S=S+U 
  return S
 def fetch_latest_code(g)->bool:
  H=urequests.get(g.firmware_url,timeout=20)
  if H.status_code==200:
   gc.collect()
   try:
    g.latest_code=H.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif H.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(g):
  with open('latest_code.py','w')as f:
   f.write(g.latest_code)
  g.current_version=g.latest_version
  with open(g.version_file,'w')as f:
   json.dump({'version':g.current_version},f)
  g.latest_code=None
  os.rename('latest_code.py',g.filename)
 def check_for_updates(g):
  print('Checking for latest version...')
  gc.collect()
  G={"accept":"application/json"}
  H=urequests.get(g.version_url,headers=G,timeout=5)
  e=json.loads(H.text)
  g.latest_version=e['oid'] 
  d=True if g.current_version!=g.latest_version else False
  T="New ver: "+str(d)
  print(T) 
  return d
 def download_and_install_update_if_available(g):
  if g.check_for_updates():
   return g.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(g):
  if g.fetch_latest_code():
   g.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

