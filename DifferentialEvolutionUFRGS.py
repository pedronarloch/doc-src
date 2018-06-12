import random
import math
from cmath import sqrt, log, cos, pi
import copy
import yaml
import time
from decimal import getcontext, Decimal
import Problems
import individuals

class DifferentialEvolution:
	getcontext().prec = 7
	
	#Common DE Parameters
	NP = 100
	F = 0.5
	CR = 1	
	MAX = 5000
	
	#Diversity Value
	m_nmdf = 0
	best_ind = []
	diversity = []
	population = []
	offspring = []
	problem = None
	strategy = 0

	def __init__(self, problem):		
		print("Differential Evolution Instancied with Problem: " + str(type(problem)))
		self.problem = problem
		self.readParameters()

	def dump(self):
		self.__init__(self.problem)
		self.m_nmdf = 0
		self.best_ind = []
		self.diversity = []
		self.population = []
		self.offspring = []

	def readParameters(self):
		with open("de_config.yaml", 'r') as stream:
			try:
				config = yaml.load(stream)
				self.NP = config['np']
				self.F = config['f']
				self.CR = config['cr']
				self.MAX = config['maxIteractions']
				self.strategy = config['strategy']
				
			except yaml.YAMLError as exc:
				print(exc)

	def initPopulation(self):
		for i in range(0, self.NP):
			ind = individuals.Individual(i)
			ind.size = self.problem.dimensions
			ind.randGen(self.problem.ub, self.problem.lb)
			ind.fitness = self.problem.evaluate(ind.dimensions)

			self.population.append(ind)

	def best1bin(self, j, trialIndividual):
		
		bestDimensions = self.population[self.getBestIndividual()].dimensions

		while 1:
			r1 = random.randint(0,self.NP-1)
			if r1 != j:
				break
		while 1:
			r2 = random.randint(0,self.NP-1)
			if r2 != j and r2 != r1:
				break

		jRand = random.randint(0,self.NP-1)

		trial = trialIndividual.dimensions
		r1Dimensions = self.population[r1].dimensions
		r2Dimensions = self.population[r2].dimensions

		for d in range(0, self.problem.dimensions):
			if random.random() <= self.CR or d == jRand:
				trial[d] = bestDimensions[d] + (self.F * (r1Dimensions[d] - r2Dimensions[d]))

		self.problem.checkBounds(trial)
		return trial

	def currToRand(self, j, trialIndividual):
		while 1:
			r1 = random.randint(0, self.NP-1)
			if r1 != j:
				break
		while 1:
			r2 = random.randint(0, self.NP-1)
			if r2 != j and r2 != r1:
				break
		while 1:
			r3 = random.randint(0, self.NP-1)
			if r3 != j and r3 != r2 and r3 != r1:
				break

		jRand = random.randint(0,self.NP-1)

		trial = trialIndividual.dimensions
		
		rCurr = self.population[j].dimensions
		r1Dimensions = self.population[r1].dimensions
		r2Dimensions = self.population[r2].dimensions
		r3Dimensions = self.population[r3].dimensions

		for d in range (0, self.problem.dimensions):
			if random.random() <= self.CR or d == jRand:
				trial[d] = rCurr[d] + (self.F * (r1Dimensions[d] - rCurr[d])) + (self.F * (r2Dimensions[d] - r3Dimensions[d]))

		self.problem.checkBounds(trial)
		return trial

	def currToBest(self, j, trialIndividual):
		bestDimensions = self.population[self.getBestIndividual()].dimensions

		while 1:
			r1 = random.randint(0, self.NP-1)
			if r1 != j:
				break

		while 1:
			r2 = random.randint(0, self.NP-1)
			if r2 != r1 and r2 != j:
				break

		jRand = random.randint(0,self.NP-1)

		trial = trialIndividual.dimensions
		r1Dimensions = self.population[r1].dimensions
		r2Dimensions = self.population[r2].dimensions

		for d in range(0, self.problem.dimensions):
			if random.random() <= self.CR or d == jRand:
				trial[d] = trial[d] + (self.F * (r1Dimensions[d] - r2Dimensions[d])) + (self.F * (bestDimensions[d] - trial[d]))

		self.problem.checkBounds(trial)

		return trial

	def randToBest(self, j, trialIndividual):
		bestDimensions = self.population[self.getBestIndividual()].dimensions

		while 1:
			r1 = random.randint(0,self.NP-1)	
			if r1 != j:
				break
		while 1:
			r2 = random.randint(0, self.NP-1)
			if r2 != j and r2 != r1:
				break
		while 1:
			r3 = random.randint(0, self.NP-1)
			if r3 != j and r3 != r1 and r3 != r2:
				break
		jRand = random.randint(0,self.NP-1)

		trial = trialIndividual.dimensions
		r1Dimensions = self.population[r1].dimensions
		r2Dimensions = self.population[r2].dimensions
		r3Dimensions = self.population[r3].dimensions

		for d in range(0, self.problem.dimensions):
			if random.random() <= self.CR or d == jRand:
				trial[d] = r1Dimensions[d] + (self.F * (r2Dimensions[d] - r3Dimensions[d])) + (self.F * (bestDimensions[d] - r1Dimensions[d]))
				
		self.problem.checkBounds(trial)

		return trial

	def rand1bin(self, j, trialIndividual):

		while 1:
			r1 = random.randint(0,self.NP-1)
			if r1 != j:
				break

		while 1:
			r2 = random.randint(0, self.NP-1)
			if r2 != j and r2 != r1:
				break

		while 1:
			r3 = random.randint(0,self.NP-1)
			if r3 != r2 and r3 != r1 and r3 != j:
				break

		jRand = random.randint(0, self.NP-1)

		trial = trialIndividual.dimensions
		r1Dimensions = self.population[r1].dimensions
		r2Dimensions = self.population[r2].dimensions
		r3Dimensions = self.population[r3].dimensions

		for d in range(0, self.problem.dimensions):						
			if random.random() <= self.CR or d == jRand:
				trial[d] = r1Dimensions[d] + (self.F * (r2Dimensions[d] - r3Dimensions[d]))

		self.problem.checkBounds(trial)

		return trial

	def getBestIndividual(self):
		bestIndex = 0
		for i in range(0, self.NP):
			if(self.population[i].fitness <= self.population[bestIndex].fitness):
				bestIndex = i

		return bestIndex

	def updateDiversity(self):
		div = 0
		aux_1 = 0
		aux_2 = 0
		a = 0
		b = 0
		d = 0

		for a in range(0, len(self.population)):
			b = a+1
			for i in range(b, len(self.population)):
				aux_1 = 0
				ind_a = self.population[self.getIndexById(a)].dimensions
				ind_b = self.population[self.getIndexById(b)].dimensions

				for d in range(0, self.problem.dimensions):
					aux_1 = aux_1 + (pow(ind_a[d] - ind_b[d], 2).real)
					aux_1 = (math.sqrt(aux_1).real)
					aux_1 = (aux_1 / self.problem.dimensions).real

				if b == i or aux_2 > aux_1:
					aux_2 = aux_1

				div = (div) + (math.log((1.0) + aux_2).real)

				if(self.m_nmdf < div):
					self.m_nmdf = div

		return (div/self.m_nmdf).real
			
	def optimize(self):
		init_time = time.time()

		self.initPopulation();

		for i in range(0, self.MAX):
			self.best_ind.append(self.population[self.getBestIndividual()])
			self.diversity.append(self.updateDiversity())

			if i % 5 == 0:
				print("Generation: ", i, " Fitness: ", self.best_ind[i].fitness, " Diversity: ", self.diversity[i], " Pop Len: ", len(self.population), "Strategy: ", self.strategy)

			if i % 100 == 0:
				print("Best Individual: ", self.best_ind[i].dimensions)

			for j in range (0, self.NP):

				trial = copy.deepcopy(self.population[j])
				
				if self.strategy == 0:
					self.rand1bin(j, trial)
				elif self.strategy == 1:
					self.currToRand(j, trial)
				elif self.strategy == 2:
					self.best1bin(j, trial)
				elif self.strategy == 3:
					self.currToBest(j, trial)
				elif self.strategy == 4:
					self.randToBest(j, trial)
				else:
					self.rand1bin(j, trial)

				trial.fitness = self.problem.evaluate(trial.dimensions)

				if trial.fitness <= self.population[j].fitness:
					self.offspring.append(trial)
				else:
					self.offspring.append(copy.copy(self.population[j]))

			self.population.clear()
			self.population = copy.copy(self.offspring)
			self.offspring.clear()

		print("Best Final Individual: ", self.best_ind[i].dimensions)
	
	def getIndexById(self, p_id):
		for i in range(0,self.NP):
			if self.population[i].indId == p_id:
				return i 
		return 0

	