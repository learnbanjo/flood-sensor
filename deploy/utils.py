q="1.0"
import gc
def qs_parse(qs):
 c={}
 W=qs.split("&")
 for k in W:
  I=k.split("=")
  if len(I)==2:
   c[I[0]]=I[1]
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

