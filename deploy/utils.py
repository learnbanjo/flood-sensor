M="1.0"
import gc
def qs_parse(qs):
 r={}
 d=qs.split("&")
 for B in d:
  n=B.split("=")
  if len(n)==2:
   r[n[0]]=n[1]
 return r
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

