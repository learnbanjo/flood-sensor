A="1.0"
import gc
def qs_parse(qs):
 v={}
 f=qs.split("&")
 for h in f:
  S=h.split("=")
  if len(S)==2:
   v[S[0]]=S[1]
 return v
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

