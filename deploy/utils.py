f="1.0"
import gc
def qs_parse(qs):
 s={}
 S=qs.split("&")
 for I in S:
  q=I.split("=")
  if len(q)==2:
   s[q[0]]=q[1]
 return s
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

