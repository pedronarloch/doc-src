import random

class Individual(object):
	
	value=[]
	fitness = 999.99

	def __init__(self):
		return 0

class DifferentialEvolution(object):

	CR = 0.0
	F = 0.0
	MAX_GEN = 0

	def __init__(self):
		return 0

	def __init__(self, cr, f, max_gen):
		self.CR = cr
		self.F = f
		self.MAX_GEN = max_gen
		return 0

	def getBestIndividual(self):
		best = 999999
		indx = 0

		for i in range(0, len(self.basePopulation)):
			if self.basePopulation.at(i).fitness <= best:
				best = self.basePopulation.at(i).fitness
				indx = i


		return self.basePopulation.at(indx)


	def rand1bin(self, j):
		newIndividual = Individual()
		r1, r2, r3 = 0
		jRand = 0 
		anglesR1, anglesR2, anglesR3 = []

		dimensionality = len(self.basePopulation.at(0).value)

		while 1:
			r1 = random.randint(0,len(self.basePopulation))			
			if r1 != j:
				break
		while 1:
			r2 = random.randint(0,len(self.basePopulation))
			if r2 != j and r2 !=  r1:
				break
		while 1:
			r3 = random.randint(0,len(self.basePopulation))
			if r3 != j and r3 != r2 and r3 != r1:
				break

		jRand = random.randint(0, dimensionality)

		anglesR1 = self.basePopulation.at(r1).value
		anglesR2 = self.basePopulation.at(r2).value
		anglesR3 = self.basePopulation.at(r3).value

		for i in range(0,dimensionality):			
			if (random.uniform(0,1) <= self.CR) or (i == jRand): #Caso a dimensionalidade tenha que ser alterada, um novo valor é composto
				newValue = anglesR1.at(i) + self.F * (anglesR2.at(i) - anglesR3.at(i))
				newIndividual.value.insert(i, newValue)
			else: #Caso essa dimensionalidade não deva ser alterada, o valor atual permanece
				newIndividual.value.insert(i, self.basePopulation.at(j).value.at(i))

		return newIndividual #retorna o novo indivíduo para OffSpring

	def best1bin(self, j):
		newIndividual = Individual()
		r1, r2 = 0
		jRand = 0
		anglesR1, anglesR2 = []

		dimensionality = len(self.basePopulation.at(0).value)

		while 1:
			r1 = random.randint(0,len(self.basePopulation))
			if r1 != j:
				break
		while 1:
			r2 = random.randint(0, len(self.basePopulation))
			if r2 != r1 and r2 != j:
				break

		jRand = random.randint(0,dimensionality)

		anglesR1 = self.basePopulation.at(r1).value
		anglesR2 = self.basePopulation.at(r2).value
		anglesBest = self.getBestIndividual().value

		for i in range(0,dimensionality):
			if (random.uniform(0,1) <= self.CR) or (i == jRand): #Caso a dimensionalidade tenha que ser alterada, um novo valor é composto
				newValue = anglesBest.at(i) + self.F * (anglesR1.at(i) - anglesR2.at(i))
				newIndividual.value.insert(i, newValue)
			else: #Caso essa dimensionalidade não deva ser alterada, o valor atual permanece
				newIndividual.value.insert(i, self.basePopulation.at(j).value(i))

		return newIndividual #retorna o novo indivíduo para OffSpring

	def optimize(self,version, initPopulation):
		finalPopulation = []
		basePopulation = copy.deepcopy(initPopulation)
		offspring = copy.deepcopy(basePopulation)

		for i in range(0,self.MAX_GEN):
			if version == 1:


			elif version == 2:


		return finalPopulation