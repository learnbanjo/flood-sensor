j="1.0"
import gc
def qs_parse(qs):
 T={}
 D=qs.split("&")
 for P in D:
  r=P.split("=")
  if len(r)==2:
   T[r[0]]=r[1]
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

