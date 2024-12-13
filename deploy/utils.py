H="1.0"
import gc
def qs_parse(qs):
 g={}
 D=qs.split("&")
 for l in D:
  W=l.split("=")
  if len(W)==2:
   g[W[0]]=W[1]
 return g
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

