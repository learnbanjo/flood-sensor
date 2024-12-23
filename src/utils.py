VERSION = "1.0"
import gc
from machine import RTC
import ntptime

def qs_parse(qs):
 
  parameters = {}
 
  ampersandSplit = qs.split("&")
 
  for element in ampersandSplit:
 
    equalSplit = element.split("=")

    if len(equalSplit) == 2:
      parameters[equalSplit[0]] = equalSplit[1]
 
  return parameters

def free(full=False):
  gc.collect()
  F = gc.mem_free()
  A = gc.mem_alloc()
  T = F+A
  P = '{0:.2f}%'.format(F/T*100)
  if not full: return P
  else : return ('Total:{0} Free:{1} ({2})'.format(T,F,P))

def get_epoch_time():

    try:
        ntptime.settime()  # Synchronize with NTP server
        rtc = RTC()
        t = rtc.datetime()
        epoch_time = (t[0]-1970) * 31536000 + t[1] * 2628000 + t[2] * 86400 + t[3] * 3600 + t[4] * 60 + t[5]
        return epoch_time
    except OSError:
        print("Error: Could not synchronize with NTP server.")
        return None
