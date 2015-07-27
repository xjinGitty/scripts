from random import random
from pprint import pprint

l1 = ['11sp3','11sp4','12']
extD = {}
extD['sp5'] = '23.45%'
for i in l1:
  intD = extD.setdefault(i,{})
  l2 = ['app','installer','gnome','desktop']
  for j in l2:
    intD[j] = str(random())[:3]


pprint(extD)

def printFD(dicD):
  for i in sorted(dicD):
    tmpD = dicD.setdefault(i,dicD[i])
    if isinstance(tmpD,dict):
      for j in sorted(tmpD):
        print("    {} | {} | {}".format(i,j,tmpD[j]))
    else:
      print("    {} | {}".format(i,dicD[i]))

printFD(extD)
    

