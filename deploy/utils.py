C="1.0"
import gc
def qs_parse(qs):
 l={}
 L=qs.split("&")
 for N in L:
  a=N.split("=")
  if len(a)==2:
   l[a[0]]=a[1]
 return l
def free(full=False):
 gc.collect()
 F=gc.mem_free()
 A=gc.mem_alloc()
 T=F+A
 P='{0:.2f}%'.format(F/T*100)
 if not full:return P
 else:return('Total:{0} Free:{1} ({2})'.format(T,F,P))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

