r="1.0"
import gc
def qs_parse(qs):
 M={}
 T=qs.split("&")
 for U in T:
  d=U.split("=")
  if len(d)==2:
   M[d[0]]=d[1]
 return M
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

