f="1.0"
import gc
def qs_parse(qs):
 T={}
 I=qs.split("&")
 for s in I:
  U=s.split("=")
  if len(U)==2:
   T[U[0]]=U[1]
 return T
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

