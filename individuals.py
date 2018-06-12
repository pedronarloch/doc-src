import random

class Individual(object):
	dimensions = []
	fitness = 0.0
	indId = 0
	size = 0

	def __init__(self, indId):
		self.dimensions = []
		self.fitness = 0.0
		self.indId = indId
		self.size = 0

	def randGen(self, ub, lb):	
		for i in range(0, self.size):			
			self.dimensions.insert(i,random.uniform(lb[i], ub[i]))

class ClusteredIndividual(Individual):
	population_id = 0

	def __init__(self, indId):
		super().__init__(indId)