x="1.0"
import gc
def qs_parse(qs):
 X={}
 y=qs.split("&")
 for B in y:
  m=B.split("=")
  if len(m)==2:
   X[m[0]]=m[1]
 return X
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

