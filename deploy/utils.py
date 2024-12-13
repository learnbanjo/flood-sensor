y="1.0"
import gc
def qs_parse(qs):
 v={}
 D=qs.split("&")
 for R in D:
  x=R.split("=")
  if len(x)==2:
   v[x[0]]=x[1]
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

