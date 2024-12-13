Y="1.0"
import gc
def qs_parse(qs):
 V={}
 J=qs.split("&")
 for l in J:
  L=l.split("=")
  if len(L)==2:
   V[L[0]]=L[1]
 return V
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

