x="1.0"
import gc
from machine import RTC
import ntptime
def qs_parse(qs):
 d={}
 t=qs.split("&")
 for T in t:
  g=T.split("=")
  if len(g)==2:
   d[g[0]]=g[1]
 return d
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
def get_epoch_time():
 try:
  ntptime.settime() 
  k=RTC()
  t=k.datetime()
  n=(t[0]-1970)*31536000+t[1]*2628000+t[2]*86400+t[3]*3600+t[4]*60+t[5]
  return n
 except OSError:
  print("Error: Could not synchronize with NTP server.")
  return None
# Created by pyminifier (https://github.com/liftoff/pyminifier)

