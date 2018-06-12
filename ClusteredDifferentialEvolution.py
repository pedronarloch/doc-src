import DifferentialEvolutionUFRGS as de

class ClusteredDifferentialEvolution(de.DifferentialEvolution):
	cluster_qty = 0

	def __init__(self, problem):
		super().__init__(problem)
		self.cluster_qty = 27


	def init_population(self):
		cluster_aux = 0
		for i in range(0, self.NP):
			ind = individuals.ClusteredIndividual(i)
			ind.size = self.problem.dimensions
			ind.rand_gen(self.problem.lb, self.problem.ub)
			ind.fitness = self.problem.evaluate(ind.dimensions)

			self.population.append(ind)