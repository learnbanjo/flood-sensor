P="1.0"
import gc
def qs_parse(qs):
 E={}
 j=qs.split("&")
 for a in j:
  S=a.split("=")
  if len(S)==2:
   E[S[0]]=S[1]
 return E
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

