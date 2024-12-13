c="1.0"
import gc
def qs_parse(qs):
 E={}
 u=qs.split("&")
 for R in u:
  N=R.split("=")
  if len(N)==2:
   E[N[0]]=N[1]
 return E
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))

