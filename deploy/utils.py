n="1.0"
import gc
def qs_parse(qs):
 u={}
 S=qs.split("&")
 for A in S:
  j=A.split("=")
  if len(j)==2:
   u[j[0]]=j[1]
 return u
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

