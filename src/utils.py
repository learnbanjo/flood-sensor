VERSION = "1.0"
import gc

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
