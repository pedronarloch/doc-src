import DifferentialEvolutionUFRGS as de

class ClusteredDifferentialEvolution(de.DifferentialEvolution):
	cluster_qty = 0

	def __init__(self, problem):
		super().__init__(problem)
		self.cluster_qty = 27
