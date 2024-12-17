O="1.0"
import gc
from machine import RTC
import ntptime
def qs_parse(qs):
 H={}
 V=qs.split("&")
 for e in V:
  P=e.split("=")
  if len(P)==2:
   H[P[0]]=P[1]
 return H
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
  f=RTC()
  t=f.datetime()
  p=(t[0]-1970)*31536000+t[1]*2628000+t[2]*86400+t[3]*3600+t[4]*60+t[5]
  return p
 except OSError:
  print("Error: Could not synchronize with NTP server.")
  return None
# Created by pyminifier (https://github.com/liftoff/pyminifier)

