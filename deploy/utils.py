T="1.0"
import gc
def qs_parse(qs):
 n={}
 S=qs.split("&")
 for i in S:
  K=i.split("=")
  if len(K)==2:
   n[K[0]]=K[1]
 return n
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

