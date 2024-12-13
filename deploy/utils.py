U="1.0"
import gc
def qs_parse(qs):
 r={}
 n=qs.split("&")
 for o in n:
  i=o.split("=")
  if len(i)==2:
   r[i[0]]=i[1]
 return r
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

