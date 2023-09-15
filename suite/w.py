#!/usr/bin/env python

import sys

fname = sys.argv[1]
fptr=open(fname)
lines=fptr.readlines()
fptr.close()
Nline=50
Nlevels=0

Nsteps=0
for line in lines:
    if line.startswith("Level"):
        Nsteps+=1
        level = int(line[6])
        Nlevels = max([level,Nlevels])
Nlevels+=1

out = [[" "]*Nsteps for n in range(Nlevels)]
counter = [0 for n in range(Nlevels)]
nstep=0
for line in lines:
    if line.startswith("Level"):
        level = int(line[6])
        out[level][nstep]="."
        print(level,nstep)
        nstep+=1
        counter[level]+=1
for nlev,level in enumerate(out):
    sss="%s"*Nsteps%tuple(level)
    print("%d %s"%(counter[nlev],sss))

            



#end
