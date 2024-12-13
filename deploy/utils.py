q="1.0"
import gc
def qs_parse(qs):
 F={}
 Y=qs.split("&")
 for U in Y:
  e=U.split("=")
  if len(e)==2:
   F[e[0]]=e[1]
 return F
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

