n="1.0"
import gc
def qs_parse(qs):
 b={}
 o=qs.split("&")
 for h in o:
  W=h.split("=")
  if len(W)==2:
   b[W[0]]=W[1]
 return b
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

