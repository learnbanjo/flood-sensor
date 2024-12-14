a="1.0"
import gc
def qs_parse(qs):
 G={}
 x=qs.split("&")
 for y in x:
  g=y.split("=")
  if len(g)==2:
   G[g[0]]=g[1]
 return G
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

