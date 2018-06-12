#import SelfAdaptiveDifferentialEvolution as sade
import DifferentialEvolutionUFRGS as de
import ClusteredDifferentialEvolution as cde
import Problems as p
import DockingProblem as docking
from decimal import getcontext, Decimal
import sys

problem = docking.DockingProblem()
algorithm = cde.ClusteredDifferentialEvolution(problem)

algorithm.optimize()


sys.exit()

#for i in range(0, 30):
#	sde.optimize()

#	convergencia = open("./1ACW-06/ALPHA_C_RUNS/RUN"+str(i)+".txt","w")
#	for k in range(0, len(sde.best_ind)):
#		convergencia.write(str(sde.best_ind[k].fitness) + "\n")
#	convergencia.close()
#	sde.dump()

#f.close()
