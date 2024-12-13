m="1.0"
import gc
def qs_parse(qs):
 c={}
 s=qs.split("&")
 for M in s:
  h=M.split("=")
  if len(h)==2:
   c[h[0]]=h[1]
 return c
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

