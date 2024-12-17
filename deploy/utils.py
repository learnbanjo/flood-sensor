F="1.0"
import gc
from machine import RTC
import ntptime
def qs_parse(qs):
 P={}
 V=qs.split("&")
 for C in V:
  j=C.split("=")
  if len(j)==2:
   P[j[0]]=j[1]
 return P
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
  O=RTC()
  t=O.datetime()
  U=(t[0]-1970)*31536000+t[1]*2628000+t[2]*86400+t[3]*3600+t[4]*60+t[5]
  return U
 except OSError:
  print("Error: Could not synchronize with NTP server.")
  return None
# Created by pyminifier (https://github.com/liftoff/pyminifier)

