w="1.0"
import gc
def qs_parse(qs):
 z={}
 I=qs.split("&")
 for Y in I:
  R=Y.split("=")
  if len(R)==2:
   z[R[0]]=R[1]
 return z
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

