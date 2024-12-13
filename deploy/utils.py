L="1.0"
import gc
def qs_parse(qs):
 m={}
 i=qs.split("&")
 for o in i:
  U=o.split("=")
  if len(U)==2:
   m[U[0]]=U[1]
 return m
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

