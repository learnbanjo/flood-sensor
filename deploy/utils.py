j="1.0"
import gc
def qs_parse(qs):
 A={}
 x=qs.split("&")
 for I in x:
  f=I.split("=")
  if len(f)==2:
   A[f[0]]=f[1]
 return A
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

