B="1.0"
import gc
def qs_parse(qs):
 n={}
 T=qs.split("&")
 for Y in T:
  o=Y.split("=")
  if len(o)==2:
   n[o[0]]=o[1]
 return n
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

