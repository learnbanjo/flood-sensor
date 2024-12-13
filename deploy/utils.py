i="1.0"
import gc
def qs_parse(qs):
 h={}
 n=qs.split("&")
 for C in n:
  c=C.split("=")
  if len(c)==2:
   h[c[0]]=c[1]
 return h
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

