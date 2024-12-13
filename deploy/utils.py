t="1.0"
import gc
def qs_parse(qs):
 E={}
 F=qs.split("&")
 for T in F:
  Y=T.split("=")
  if len(Y)==2:
   E[Y[0]]=Y[1]
 return E
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

