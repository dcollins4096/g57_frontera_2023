
from GL import *
import performance_tools as pt
reload(pt)
plt.close('all')
if 1:

    base_dir="../suite"
    suite_list=['MHD','Grav','AMR']
    side_list = [64,128]
    pdict={}

    for suite in suite_list:
        pdict[suite]={}
        for side in side_list:
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
            zone_up_su['Total'].append( sim.data['Total']['Updates/processor/sec'].mean())
            zone_up_su['Level 00'].append( sim.data['Level 00']['Updates/processor/sec'].mean())
            mpi_tasks.append( sim.data['mpi_tasks'])


        for key in ['Level 00']: #zone_up_su:
            #ax_zu.plot(mean_time['mpi_tasks'],zone_up_su[key],label="%s %s"%(key,suite_name), marker='*')
            print( suite_name, key)
            print(zone_up_su[key])
            ax_zu.plot(mpi_tasks,zone_up_su[key],label=suite_name, marker='*')



ax_zu.legend(loc=0)
ax_zu.set(xlabel=lab_mpi, ylabel=r'$\rm{(zone\ updates)/(core\ second)}$',xscale='log',yscale='log', ylim=[1e4,2e5])
outname = '%s/%s/g57_zoneup.pdf'%(os.environ['HOME'],'PigPen')
fig_zu.savefig(outname)
print(outname)
plt.close(fig_zu)
