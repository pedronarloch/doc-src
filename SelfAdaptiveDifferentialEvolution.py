import DifferentialEvolutionUFRGS as de
import Problems
import random
import time
import copy
import yaml
import sys

class SADE(de.DifferentialEvolution):

	LP = 0 #Learning stage generations
	CRm = 0.5 #Crossover memory
	CRs = []
	ns = [] #sucessfull rating
	nf = [] #fails rating
	probs = [] #probabilities
	mutationQtd = 1

	def __init__(self, problem):
		print("Self Adaptive Differential Evolution Instancied with Problem: " + str(type(problem)))
		self.problem = problem
		self.readParameters()
		for i in range(0, self.mutationQtd):
			self.ns.append(0)
			self.nf.append(0)		
			self.probs.append(1/self.mutationQtd)

	def readParameters(self):
		with open("de_config.yaml", 'r') as stream:
			try:
				config = yaml.load(stream)
				self.NP = config['np']
				self.F = config['f']
				self.CR = config['cr']
				self.MAX = config['maxIteractions']
				self.mutationQtd = config['strategy']
				self.LP = config['lp']

			except yaml.YAMLError as exc:
				print(exc)
		
	def learningProcess(self):	
		acum_prob = 0
		self.best_ind.clear()
		self.diversity.clear()
		self.m_nmdf = 0

		self.initPopulation()

		for i in range(0, self.LP):

			self.best_ind.append(self.population[self.getBestIndividual()])
			self.diversity.append(self.updateDiversity())

			if i % 25 == 0 and i > 0:
				self.CRm = sum(self.CRs)/len(self.CRs)
				self.CRs.clear()

			if i % 5 == 0:
				self.CR = -1
				while(self.CR < 0):
					self.CR = random.gauss(self.CRm, 0.1)

				print("Learning Generation: ", i, " Energy: ", self.best_ind[i].fitness, " Diversity: ", self.diversity[i], " Pop Len: ", len(self.population), " Strategy: ", self.strategy, " CRm: ", self.CRm)

			for j in range (0, self.NP):

				rand_strategy = random.uniform(0,1)
				acum_prob = 0

				for sp in range(0, self.mutationQtd):

					acum_prob += self.probs[sp]

					#print(str(rand_strategy) + " : " + str(acum_prob))

					if(rand_strategy < acum_prob):
						#print("Estratégia Selecionada: " + str(sp))
						self.strategy = sp
						break

				self.F = -1
				while(self.F < 0):
					self.F = random.gauss(0.5, 0.3)

				result = self.evolve(j) #Evolve process, it returns True if the new individual is better than the older one. False otherwise

				if(result == True):
					self.ns[self.strategy] += 1
					self.CRs.append(self.CR)
				else:
					self.nf[self.strategy] += 1

			self.updateProbabilities()
			self.population.clear()
			self.population = copy.copy(self.offspring)
			self.offspring.clear()


	def updateProbabilities(self):
		total = 0
		local_percent = []
		for i in range(0, self.mutationQtd):
			if(self.ns[i] + self.nf[i] != 0):
				local_percent.append(self.ns[i] / (self.ns[i]+self.nf[i]))
				total += local_percent[i]
			else:
				print("O metodo " + str(i) + " obteve apenas falhas: " + str(self.nf[i]))
				local_percent.append(0)

		for i in range(0, self.mutationQtd):
			self.probs[i] = local_percent[i]/total

	def optimize(self):
		init_time = time.time()		
		result = False
		
		self.learningProcess() #Learning phase
		
		print(self.probs)

		self.m_nmdf = 0
		self.CRm = 0.5
		self.CRs.clear()
		self.population.clear()
		self.offspring.clear()
		self.best_ind.clear()
		self.diversity.clear()

		self.initPopulation()

		for i in range(0, self.MAX):
			self.best_ind.append(self.population[self.getBestIndividual()])
			self.diversity.append(self.updateDiversity())

			if i % 25 == 0 and i > 0:
				self.CRm = sum(self.CRs)/len(self.CRs)
				self.CRs.clear()

			if i % 5 == 0:
				self.CR = -1
				while(self.CR < 0):
					self.CR = random.gauss(self.CRm, 0.1)

				print("Generation: ", i, " Energy: ", self.best_ind[i].fitness, " Diversity: ", self.diversity[i], " Pop Len: ", len(self.population), " Strategy: ", self.strategy, " CRm: ", self.CRm)

			for j in range (0, self.NP):

				rand_strategy = random.uniform(0,1)
				acum_prob = 0

				for sp in range(0, self.mutationQtd):

					acum_prob += self.probs[sp]

					if(rand_strategy < acum_prob):
						self.strategy = sp
						break
				
				self.F = -1
				while(self.F < 0):
					self.F = random.gauss(0.5, 0.3)

				result = self.evolve(j)

				if(result == True):
					self.ns[self.strategy] += 1
					self.CRs.append(self.CR)
				else:
					self.nf[self.strategy] += 1

			self.updateProbabilities()

			self.population.clear()
			self.population = copy.copy(self.offspring)
			self.offspring.clear()

	def evolve(self, j):

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
				return True
			else:
				self.offspring.append(copy.copy(self.population[j]))
				return False