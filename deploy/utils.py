X="1.0"
import gc
from machine import RTC
import ntptime
def qs_parse(qs):
 x={}
 j=qs.split("&")
 for R in j:
  H=R.split("=")
  if len(H)==2:
   x[H[0]]=H[1]
 return x
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
  z=RTC()
  t=z.datetime()
  l=(t[0]-1970)*31536000+t[1]*2628000+t[2]*86400+t[3]*3600+t[4]*60+t[5]
  return l
 except OSError:
  print("Error: Could not synchronize with NTP server.")
  return None
# Created by pyminifier (https://github.com/liftoff/pyminifier)

