D="1.0"
import gc
def qs_parse(qs):
 R={}
 F=qs.split("&")
 for P in F:
  J=P.split("=")
  if len(J)==2:
   R[J[0]]=J[1]
 return R
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

