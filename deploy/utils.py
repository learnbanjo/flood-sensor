M="1.0"
import gc
def qs_parse(qs):
 W={}
 r=qs.split("&")
 for L in r:
  D=L.split("=")
  if len(D)==2:
   W[D[0]]=D[1]
 return W
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

