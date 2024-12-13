y="1.0"
import gc
def qs_parse(qs):
 F={}
 e=qs.split("&")
 for W in e:
  z=W.split("=")
  if len(z)==2:
   F[z[0]]=z[1]
 return F
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

