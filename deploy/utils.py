a="1.0"
import gc
def qs_parse(qs):
 H={}
 N=qs.split("&")
 for h in N:
  u=h.split("=")
  if len(u)==2:
   H[u[0]]=u[1]
 return H
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

