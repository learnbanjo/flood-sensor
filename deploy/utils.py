V="1.0"
import gc
def qs_parse(qs):
 B={}
 F=qs.split("&")
 for c in F:
  M=c.split("=")
  if len(M)==2:
   B[M[0]]=M[1]
 return B
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

