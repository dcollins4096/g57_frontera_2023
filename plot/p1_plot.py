
from GL import *
import yt


sim = "../suite/AMR2/AMR2_256"

ds = yt.load("%s/DD%04d/data%04d"%(sim,0,0))
proj = yt.ProjectionPlot(ds,0,'density')
proj.annotate_grids()
outname = '%s/%s/thing'%(os.environ['HOME'],'PigPen')
proj.save(outname)

