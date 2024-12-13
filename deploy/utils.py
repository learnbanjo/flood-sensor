g="1.0"
import gc
def qs_parse(qs):
 U={}
 X=qs.split("&")
 for Y in X:
  T=Y.split("=")
  if len(T)==2:
   U[T[0]]=T[1]
 return U
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

