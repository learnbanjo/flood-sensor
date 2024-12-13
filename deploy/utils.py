L="1.0"
import gc
def qs_parse(qs):
 Y={}
 z=qs.split("&")
 for T in z:
  r=T.split("=")
  if len(r)==2:
   Y[r[0]]=r[1]
 return Y
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

