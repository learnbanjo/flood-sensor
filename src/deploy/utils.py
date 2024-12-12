z="1.0"
import gc
def qs_parse(qs):
 V={}
 P=qs.split("&")
 for i in P:
  K=i.split("=")
  if len(K)==2:
   V[K[0]]=K[1]
 return V
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))

