#!/usr/bin/env python
import numpy as np
import sys
import os
import shutil
import jinja2
import glob


def amr_stack_2():
    #for AMR5
    #right=[ 0.01220703125, 0.01318359375, 0.0146484375, 0.015625, 0.03125, 0.0625, 0.125, 0.25, 0.5][::-1]
    #top=[0.0001220703125, 0.000732421875, 0.00537109375, 0.015625, 0.03125, 0.0625, 0.125, 0.25, 0.5][::-1]
    right=[0.006103515625, 0.006591796875, 0.00732421875, 0.0078125, 0.015625, 0.03125, 0.0625, 0.125, 0.25, 0.5][::-1]
    top=[0.00006103515625, 0.0003662109375, 0.002685546875, 0.0078125, 0.015625, 0.03125, 0.0625, 0.125, 0.25, 0.5][::-1]
    output=""
    region=0
    for n in range(len(right)):
        if n==0:
            #dont need top grid
            continue
        L = -right[n]
        R = right[n]
        T = top[n]
        B = -top[n]
        level=n-1
        output+="StaticRefineRegionLevel[%d]  =   %d\n"%(region,level)       
        output+="StaticRefineRegionLeftEdge[%d]   =   %.16f %.16f %.16f\n"%(region,L,L,B)
        output+="StaticRefineRegionRightEdge[%d]  =   %.16f %.16f %.16f\n"%(region,R,R,T)
        region+=1
    return output

def amr_stack(nlevels):
    output=""
    region=-1
    for level in np.arange(nlevels):
        region=region+1
        left = 0.5-0.5**(level+2)
        right = 0.5+0.5**(level+2)
        print(left)
        output+="StaticRefineRegionLevel[%d]  =   %d\n"%(region,level)       
        output+="StaticRefineRegionLeftEdge[%d]   =   %.16f %.16f %.16f\n"%(region,left,left,left)
        output+="StaticRefineRegionRightEdge[%d]  =   %.16f %.16f %.16f\n"%(region,right,right,right)
    return output


if len(sys.argv) != 2:
    print("manager.py {Grav AMR MHD}")
    print("call from one of {Grav AMR MHD} as ")
    print(" ../manager.py AMR")
    sys.exit(0)
else:
    base = sys.argv[1]

do_amr_stack=False
if base == 'AMR3':
    do_amr_stack=True
    Nlevels=6
    amr = amr_stack(Nlevels)
if base == 'AMR5':
    do_amr_stack=True
    Nlevels=8
    amr = amr_stack_2()#lazy programmer, hard coded things.
if base == 'AMR6':
    do_amr_stack=True
    Nlevels=9
    amr = amr_stack_2()
cores_per_node=56.
template_file_enzo = 'template_%s.enzo'%base
template_file_sbatch = "template.sbatch"
template_file_m = "template.m"
zones_per_grid=64
#sidelist=[256, 512, 1024, 1536, 2048]
sidelist=[256,512,1024]
#sidelist=[64, 128]
for nside in sidelist:
    ntask_per_side = max([nside//zones_per_grid,1])
    ntask = ntask_per_side**3   
    N = int(np.ceil(ntask/cores_per_node))
    print("ntask %d N %d ntask/core_per_node %f"%(ntask,N, ntask/cores_per_node))
    task_per_node = min([cores_per_node, ntask])

    dirname = "run_%s_%d"%(base,nside)
    simname = "%s"%(base)
    pf_name = "%s.enzo"%(simname)
    sbatch_name = "%s.sbatch"%(simname)
    jobname = "%s_%d"%(base,nside)

    fname_enzo = "%s/%s"%(dirname, pf_name)
    fname_sbatch = "%s/%s"%(dirname, sbatch_name)
    fname_m = "%s/m.local"%(dirname)

    kwargs_enzo = {}
    kwargs_enzo['TopGridDimensions'] = "%d %d %d"%(nside,nside,nside)
    kwargs_enzo['TracerSpacing'] = "%f"%(1./nside)

    if do_amr_stack:
        kwargs_enzo['maximum_refinement']=Nlevels
        kwargs_enzo['refinement_regions']=amr
        print(amr)


    kwargs_sbatch = {}
    kwargs_sbatch['jobname'] = jobname
    kwargs_sbatch['Nnodes'] = int(N)
    kwargs_sbatch['ncores'] = ntask
    kwargs_sbatch['tasks_per_node'] = int(task_per_node)
    kwargs_sbatch['enzo_parameter'] = pf_name
    if N < 3:
        queue = "flex"
    elif N < 512:
        queue = "normal"
    else:
        queue = "large"
    kwargs_sbatch['queue']=queue
    print("queue",queue)

    kwargs_m={}
    kwargs_m['enzo_parameter']=pf_name
    kwargs_m['ncores']=ntask


    if not os.path.exists( dirname ):
        os.mkdir(dirname)

    loader=jinja2.FileSystemLoader('.')
    env = jinja2.Environment(loader=loader)

    template_m = env.get_template(template_file_m)
    foutptr = open(fname_m,'w')
    foutptr.write( template_m.render(**kwargs_m))
    foutptr.close()
    print("wrote %s"%fname_m)

    template_enzo = env.get_template(template_file_enzo)
    foutptr = open(fname_enzo,'w')
    foutptr.write( template_enzo.render(**kwargs_enzo))
    foutptr.close()
    print("wrote %s"%fname_enzo)

    template_sbatch = env.get_template(template_file_sbatch)
    foutptr = open(fname_sbatch,'w')
    foutptr.write( template_sbatch.render(**kwargs_sbatch))
    foutptr.close()
    print("wrote %s"%fname_sbatch)

    shutil.copy("enzo.exe", "%s/enzo.exe"%(dirname))

    for fil in glob.glob('fiducial/*'):
        file_base = fil.split("/")[-1]
        shutil.copy( fil, "%s/%s"%(dirname,file_base))
    print("copied enzo.exe")
