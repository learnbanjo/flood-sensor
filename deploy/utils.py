T="1.0"
import gc
from machine import RTC
import ntptime
def qs_parse(qs):
 L={}
 a=qs.split("&")
 for D in a:
  x=D.split("=")
  if len(x)==2:
   L[x[0]]=x[1]
 return L
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
  y=RTC()
  t=y.datetime()
  h=(t[0]-1970)*31536000+t[1]*2628000+t[2]*86400+t[3]*3600+t[4]*60+t[5]
  return h
 except OSError:
  print("Error: Could not synchronize with NTP server.")
  return None
# Created by pyminifier (https://github.com/liftoff/pyminifier)

