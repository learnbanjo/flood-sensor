q="1.0"
import gc
def qs_parse(qs):
 D={}
 g=qs.split("&")
 for c in g:
  X=c.split("=")
  if len(X)==2:
   D[X[0]]=X[1]
 return D
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

