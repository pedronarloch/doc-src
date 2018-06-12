import SelfAdaptiveDifferentialEvolution as sade
import DifferentialEvolutionUFRGS as de
import Problems as p
import rmsd_problem as rmsd
from decimal import getcontext, Decimal

pB = rmsd.RMSD_Problem()
sde = de.DifferentialEvolution(pB)

for i in range(0, 30):
	sde.optimize()

	convergencia = open("./1ACW-06/ALPHA_C_RUNS/RUN"+str(i)+".txt","w")
	for k in range(0, len(sde.best_ind)):
		convergencia.write(str(sde.best_ind[k].fitness) + "\n")
	convergencia.close()
	sde.dump()

#f.close()
