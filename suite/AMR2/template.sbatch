#!/bin/tcsh
#----------------------------------------------------
# Example SLURM job script to run multiple mpi
# applications within one batch job on TACC's
# Stampede system.
#----------------------------------------------------
#SBATCH -J {{jobname}}     # Job name
#SBATCH -o {{jobname}}.o%j # Name of stdout output file(%j expands to jobId)
#SBATCH -e {{jobname}}.o%j # Name of stderr output file(%j expands to jobId)
#SBATCH -p {{queue}}          # Submit to the 'normal' or 'development' queue
#SBATCH -t 00:20:00             # Run time (hh:m) - 1.5 hours
#SBATCH -N {{Nnodes}}                    # Total number of nodes requested (16 cores/node)
#SBATCH -n {{ncores}}                   # Total number of mpi tasks requested
#SBATCH --tasks-per-node {{tasks_per_node}}
#SBATCH --mail-user=dccollins@fsu.edu
#SBATCH --mail-type=begin  # email me when the job starts
#SBATCH --mail-type=end    # email me when the job finishes
# The next line is required if the user has more than one project

#USAGE 
#Fix the node count and time above.
#Make sure enzo is built and in the working directory.
#Make sure the parameter field on the ibrun  line.

set echo
#module load hdf5/1.8
ibrun ./enzo.exe -d {{enzo_parameter}}

