
from GL import *
import performance_tools as pt
reload(pt)
plt.close('all')
if 1:

    base_dir="../suite"
    suite_list=['MHD','Grav', 'AMR1']#,'AMR']
    side_list={}
    side_list['Grav']= [256, 512]
    side_list['AMR']= [256, 512]
    #side_list['MHD']= [256, 512, 1024, 1536, 2048]
    side_list['MHD']= [256, 512, 1024, 1536, 2048]
    side_list['Grav']= [256, 512, 1024, 1536, 2048]
    #side_list['AMR']= [256, 512]#, 1024, 1536]
    side_list['AMR1']= [256, 512, 1024, 1536]
    pdict={}
    zeta={}

    for suite in suite_list:
        pdict[suite]={}
        zeta[suite]={}
        for side in side_list[suite]:
            name = "%s_%d"%(suite,side)
            directory = "%s/%s/%s"%(base_dir,suite,name)
            pdict[suite][name] = pt.perform("%s/performance.out"%directory)


lab_mpi=r'$\rm{mpi\ tasks}$'
fig_zu,ax_zu=plt.subplots(1,1)

if 1:
    for suite_name in pdict:
        print("suite "+suite_name)
        suite = pdict[suite_name]
        zone_up_su = {}
        mpi_tasks=[]
        for key in ['Total','Level 00']:
            zone_up_su[key]=[]
        for simname in suite:
            sim=suite[simname]
            total= sim.data['Total']['Updates/processor/sec'].mean()
            zone_up_su['Total'].append(total)
            L0= sim.data['Level 00']['Updates/processor/sec'].mean()
            zone_up_su['Level 00'].append(L0)
            NC= sim.data['mpi_tasks']
            mpi_tasks.append(NC)
            zeta[suite_name][NC]=L0


        WHAT_TO_PLOT = "Total"
        WHAT_TO_PLOT = "Level 00"
        for key in [WHAT_TO_PLOT]: #zone_up_su:
            #ax_zu.plot(mean_time['mpi_tasks'],zone_up_su[key],label="%s %s"%(key,suite_name), marker='*')
            print( suite_name, key)
            ntask = len(zone_up_su[key])
            print("ZU/SU" + " %0.1e"*ntask%tuple(zone_up_su[key]))
            ax_zu.plot(mpi_tasks,zone_up_su[key],label=suite_name, marker='*')
            print(mpi_tasks)

ax_zu.scatter( 512, zeta['AMR1'][512], s=100, facecolor='none', edgecolor='r')
ncores = max(zeta['MHD'].keys())
ax_zu.scatter( ncores, zeta['MHD'][ncores], s=100, facecolor='none', edgecolor='r')
print("WTF", zeta['MHD'][512], ncores)

ax_zu.legend(loc=0)
ax_zu.set(xlabel=r'$N_C$', ylabel=r'$\rm{(zone\ updates)/(core\ second)}$',xscale='log',yscale='log')
outname = '%s/%s/g57_zoneup.pdf'%(os.environ['HOME'],'PigPen')
fig_zu.savefig(outname)
print(outname)
plt.close(fig_zu)
