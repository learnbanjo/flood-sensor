T="1.0"
import gc
def qs_parse(qs):
 J={}
 v=qs.split("&")
 for U in v:
  N=U.split("=")
  if len(N)==2:
   J[N[0]]=N[1]
 return J
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

