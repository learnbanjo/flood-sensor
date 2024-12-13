E="1.0"
import gc
def qs_parse(qs):
 p={}
 r=qs.split("&")
 for K in r:
  f=K.split("=")
  if len(f)==2:
   p[f[0]]=f[1]
 return p
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

