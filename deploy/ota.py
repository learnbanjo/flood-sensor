import urequests
import os
import gc
import json
N="1.0"
class OTAUpdater:
 def __init__(G,i,X):
  G.filename=X
  G.repo_url=i
  G.version_file=X+'_'+'ver.json'
  G.version_url=G.process_version_url(i,X) 
  G.firmware_url=i+X 
  if G.version_file in os.listdir():
   with open(G.version_file)as f:
    G.current_version=json.load(f)['version']
  else:
   G.current_version="0"
   with open(G.version_file,'w')as f:
    json.dump({'version':G.current_version},f)
 def process_version_url(G,i,X):
  c=i.replace("raw.githubusercontent.com","github.com") 
  c=c.replace("/","§",4) 
  c=c.replace("/","/latest-commit/",1) 
  c=c.replace("§","/",4) 
  c=c+X 
  return c
 def fetch_latest_code(G)->bool:
  g=urequests.get(G.firmware_url,timeout=20)
  if g.status_code==200:
   gc.collect()
   try:
    G.latest_code=g.text
    return True
   except Exception as e:
    print('Failed to fetch latest code:',e)
    return False
  elif g.status_code==404:
   print('Firmware not found.')
   return False
 def update_no_reset(G):
  with open('latest_code.py','w')as f:
   f.write(G.latest_code)
  G.current_version=G.latest_version
  with open(G.version_file,'w')as f:
   json.dump({'version':G.current_version},f)
  G.latest_code=None
  os.rename('latest_code.py',G.filename)
 def check_for_updates(G):
  gc.collect()
  r={"accept":"application/json"}
  g=urequests.get(G.version_url,headers=r,timeout=5)
  v=json.loads(g.text)
  G.latest_version=v['oid'] 
  E=True if G.current_version!=G.latest_version else False
  n="New ver: "+str(E)
  print(n) 
  return E
 def download_and_install_update_if_available(G):
  if G.check_for_updates():
   return G.download_and_install_update()
  else:
   print('No new updates available.')
   return True
 def download_and_install_update(G):
  if G.fetch_latest_code():
   G.update_no_reset()
  else:
   return False
  return True
# Created by pyminifier (https://github.com/liftoff/pyminifier)

