t="1.0"
import gc
def qs_parse(qs):
 B={}
 i=qs.split("&")
 for M in i:
  w=M.split("=")
  if len(w)==2:
   B[w[0]]=w[1]
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

