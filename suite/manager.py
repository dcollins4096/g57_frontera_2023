#!/usr/bin/env python
import numpy as np
import sys
import os
import shutil
import jinja2
import glob


if len(sys.argv) != 2:
    print("manager.py {Grav AMR MHD}")
    print("call from one of {Grav AMR MHD} as ")
    print(" ../manager.py AMR")
    sys.exit(0)
else:
    base = sys.argv[1]
cores_per_node=56
template_file_enzo = 'template_%s.enzo'%base
template_file_sbatch = "template.sbatch"
template_file_m = "template.m"
zones_per_grid=64
sidelist=[256, 512, 1024, 1536, 2040]
sidelist=[32]
sidelist=[64, 128]
for nside in sidelist:
    ntask_per_side = max([nside//zones_per_grid,1])
    ntask = ntask_per_side**3   
    N = max([ntask//cores_per_node,1])
    task_per_node = min([cores_per_node, ntask])

    dirname = "%s_%d"%(base,nside)
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

    kwargs_sbatch = {}
    kwargs_sbatch['jobname'] = jobname
    kwargs_sbatch['Nnodes'] = N
    kwargs_sbatch['ncores'] = ntask
    kwargs_sbatch['tasks_per_node'] = task_per_node
    kwargs_sbatch['enzo_parameter'] = pf_name

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
