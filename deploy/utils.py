f="1.0"
import gc
def qs_parse(qs):
 C={}
 c=qs.split("&")
 for u in c:
  H=u.split("=")
  if len(H)==2:
   C[H[0]]=H[1]
 return C
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

