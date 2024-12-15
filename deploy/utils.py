V="1.0"
import gc
def qs_parse(qs):
 c={}
 v=qs.split("&")
 for H in v:
  k=H.split("=")
  if len(k)==2:
   c[k[0]]=k[1]
 return c
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

