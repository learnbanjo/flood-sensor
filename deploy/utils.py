c="1.0"
import gc
def qs_parse(qs):
 v={}
 K=qs.split("&")
 for a in K:
  G=a.split("=")
  if len(G)==2:
   v[G[0]]=G[1]
 return v
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

