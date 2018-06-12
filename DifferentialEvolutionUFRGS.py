import random
import math
from cmath import sqrt, log, cos, pi
import copy
import yaml
import time
from decimal import getcontext, Decimal
import Problems
import individuals
import sys

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
		self.read_parameters()

	def dump(self):
		self.__init__(self.problem)
		self.m_nmdf = 0
		self.best_ind = []
		self.diversity = []
		self.population = []
		self.offspring = []

	def read_parameters(self):
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
				sys.exit()
				
	def init_population(self):
		for i in range(0, self.NP):
			ind = individuals.Individual(i)
			ind.size = self.problem.dimensions
			ind.rand_gen(self.problem.ub, self.problem.lb)
			ind.fitness = self.problem.evaluate(ind.dimensions)

			self.population.append(ind)

	#Random Canonical Selection 
	def selection_operator(self):
		return random.randint(0, self.NP-1)		

	def best_1_bin(self, j, trial_individual):
		
		bestDimensions = self.population[self.get_best_individual()].dimensions

		while 1:
			r1 = self.selection_operator()
			if r1 != j:
				break
		while 1:
			r2 = self.selection_operator()
			if r2 != j and r2 != r1:
				break

		jRand = random.randint(0,self.problem.dimensions-1)

		trial = trial_individual.dimensions
		r1_dimensions = self.population[r1].dimensions
		r2_dimensions = self.population[r2].dimensions

		for d in range(0, self.problem.dimensions):
			if random.random() <= self.CR or d == jRand:
				trial[d] = best_dimensions[d] + (self.F * (r1_dimensions[d] - r2_dimensions[d]))

		self.problem.check_bounds(trial)

		return trial

	def curr_to_rand(self, j, trial_individual):
		while 1:
			r1 = self.selection_operator()
			if r1 != j:
				break
		while 1:
			r2 = self.selection_operator()
			if r2 != j and r2 != r1:
				break
		while 1:
			r3 = self.selection_operator()
			if r3 != j and r3 != r2 and r3 != r1:
				break

		jRand = random.randint(0,self.problem.dimensions-1)

		trial = trial_individual.dimensions
		
		r_curr = self.population[j].dimensions
		r1_dimensions = self.population[r1].dimensions
		r2_dimensions = self.population[r2].dimensions
		r3_dimensions = self.population[r3].dimensions

		for d in range (0, self.problem.dimensions):
			if random.random() <= self.CR or d == jRand:
				trial[d] = r_curr[d] + (self.F * (r1_dimensions[d] - r_curr[d])) + (self.F * (r2_dimensions[d] - r3_dimensions[d]))

		self.problem.check_bounds(trial)

		return trial

	def curr_to_best(self, j, trial_individual):
		best_dimensions = self.population[self.get_best_individual()].dimensions

		while 1:
			r1 = self.selection_operator()
			if r1 != j:
				break

		while 1:
			r2 = self.selection_operator()
			if r2 != r1 and r2 != j:
				break

		jRand = random.randint(0,self.problem.dimensions-1)

		trial = trial_individual.dimensions
		r1_dimensions = self.population[r1].dimensions
		r2_dimensions = self.population[r2].dimensions

		for d in range(0, self.problem.dimensions):
			if random.random() <= self.CR or d == jRand:
				trial[d] = trial[d] + (self.F * (r1_dimensions[d] - r2_dimensions[d])) + (self.F * (best_dimensions[d] - trial[d]))

		self.problem.check_bounds(trial)

		return trial

	def rand_to_best(self, j, trial_individual):
		best_dimensions = self.population[self.get_best_individual()].dimensions

		while 1:
			r1 = self.selection_operator()
			if r1 != j:
				break
		while 1:
			r2 = self.selection_operator()
			if r2 != j and r2 != r1:
				break
		while 1:
			r3 = self.selection_operator()
			if r3 != j and r3 != r1 and r3 != r2:
				break
		jRand = self.selection_operator()

		trial = trial_individual.dimensions
		r1_dimensions = self.population[r1].dimensions
		r2_dimensions = self.population[r2].dimensions
		r3_dimensions = self.population[r3].dimensions

		for d in range(0, self.problem.dimensions):
			if random.random() <= self.CR or d == jRand:
				trial[d] = r1_dimensions[d] + (self.F * (r2_dimensions[d] - r3_dimensions[d])) + (self.F * (best_dimensions[d] - r1_dimensions[d]))
				
		self.problem.check_bounds(trial)

		return trial

	def rand_1_bin(self, j, trial_individual):

		while 1:
			r1 = self.selection_operator()
			if r1 != j:
				break

		while 1:
			r2 = self.selection_operator()
			if r2 != j and r2 != r1:
				break

		while 1:
			r3 = self.selection_operator()
			if r3 != r2 and r3 != r1 and r3 != j:
				break

		jRand = random.randint(0, self.problem.dimensions-1)

		trial = trial_individual.dimensions
		r1_dimensions = self.population[r1].dimensions
		r2_dimensions = self.population[r2].dimensions
		r3_dimensions = self.population[r3].dimensions

		for d in range(0, self.problem.dimensions):						
			if random.random() <= self.CR or d == jRand:
				trial[d] = r1_dimensions[d] + (self.F * (r2_dimensions[d] - r3_dimensions[d]))

		self.problem.checkBounds(trial)

		return trial

	def get_best_individual(self):
		best_index = 0
		for i in range(0, self.NP):
			if(self.population[i].fitness <= self.population[best_index].fitness):
				best_index = i

		return best_index

	def update_diversity(self):
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
				ind_a = self.population[self.get_index_by_id(a)].dimensions
				ind_b = self.population[self.get_index_by_id(b)].dimensions

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

		self.init_population();

		for i in range(0, self.MAX):
			self.best_ind.append(self.population[self.get_best_individual()])
			self.diversity.append(self.update_diversity())

			if i % 5 == 0:
				print("Generation: ", i, " Fitness: ", self.best_ind[i].fitness, " Diversity: ", self.diversity[i], " Pop Len: ", len(self.population), "Strategy: ", self.strategy)

			if i % 100 == 0:
				print("Best Individual: ", self.best_ind[i].dimensions)

			for j in range (0, self.NP):

				trial = copy.deepcopy(self.population[j])
				
				if self.strategy == 0:
					self.rand_1_bin(j, trial)
				elif self.strategy == 1:
					self.curr_to_rand(j, trial)
				elif self.strategy == 2:
					self.best_1_bin(j, trial)
				elif self.strategy == 3:
					self.curr_to_best(j, trial)
				elif self.strategy == 4:
					self.rand_to_best(j, trial)
				else:
					self.rand_1_bin(j, trial)

				trial.fitness = self.problem.evaluate(trial.dimensions)

				if trial.fitness <= self.population[j].fitness:
					self.offspring.append(trial)
				else:
					self.offspring.append(copy.copy(self.population[j]))

			self.population.clear()
			self.population = copy.copy(self.offspring)
			self.offspring.clear()

		print("Best Final Individual: ", self.best_ind[i].dimensions)
	
	def get_index_by_id(self, p_id):
		for i in range(0,self.NP):
			if self.population[i].indId == p_id:
				return i 
		return 0

	