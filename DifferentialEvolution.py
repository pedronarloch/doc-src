import random
import math
from cmath import sqrt, log, cos, pi
import copy
import yaml
import pyrosetta
import time
from decimal import getcontext, Decimal

class AminoAcid:
	numAngles = 0
	angles = []
	secondaryStructure = ""
	name = ""

	def __init__(self, aminoName, aminoStructure):
		self.angles = []
		self.numAngles = 0
		self.name = aminoName
		self.secondaryStructure = aminoStructure
		self.numAngles = 2 + self.getNumSideChainAngles()
		self.generateRandomAngles()

	def generateRandomAngles(self):
		angle = 0
		for i in range(0, self.numAngles):
			if (i < 2):			
				self.angles.insert(i, Decimal(random.uniform(self.getSecondaryLowerBound(i), self.getSecondaryUpperBound(i)))/1)
			elif (i >= 2):		
				self.angles.insert(i, Decimal(random.uniform(self.getSideChainLowerBound(i), self.getSideChainUpperBound(i)))/1)


	def getNumSideChainAngles(self):
		if (self.name == 'GLY' or self.name == 'G') or (self.name == 'ALA' or self.name == 'A') or (self.name == 'PRO' or self.name =='P'):
			return 0
		elif (self.name == 'SER' or self.name == 'S') or (self.name == 'CYS' or self.name == 'C') or (self.name == "THR" or self.name == 'T') or (self.name == 'VAL' or self.name == 'V'):
			return 1
		elif (self.name == 'ILE' or self.name == 'I') or (self.name == 'LEU' or self.name == 'L') or (self.name == 'ASP' or self.name == 'D') or (self.name == 'ASN' or self.name == 'N') or (self.name == 'PHE' or self.name == 'F') or (self.name == 'TYR' or self.name == 'Y') or (self.name == 'HIS' or self.name == 'H') or (self.name == 'TRP' or self.name == 'W'):
			return 2
		elif (self.name == 'MET' or self.name == 'M') or (self.name == 'GLU' or self.name == 'E') or (self.name == 'GLN' or self.name == 'Q'):
			return 3
		elif (self.name == 'LYS' or self.name == 'K') or (self.name == 'ARG' or self.name == 'R'):
			return 4
		return 0

	def getSecondaryLowerBound(self, i):
		if self.secondaryStructure == "H":
			if i == 0:
				return -67
			elif i == 1:
				return -57
		elif self.secondaryStructure == "B" or self.secondaryStructure == "E":
			if i == 0:
				return -130
			elif i == 1:
				return 110
		elif self.secondaryStructure == "G":
			if i == 0:
				return -59
			elif i == 1:
				return -36
		elif self.secondaryStructure == "I":
			if i == 0:
				return -67
			elif i == 1:
				return -80
		elif self.secondaryStructure == "T" or self.secondaryStructure == "S" or self.secondaryStructure == "C":
			return -180

	def getSecondaryUpperBound(self, i):
		if self.secondaryStructure == "H":
			if i == 0:
				return -47
			elif i == 1:
				return -37
		elif self.secondaryStructure == "B" or self.secondaryStructure == "E":
			if i == 0:
				return -110
			elif i == 1:
				return 130
		elif self.secondaryStructure == "G":
			if i == 0:
				return -39
			elif i == 1:
				return 16
		elif self.secondaryStructure == "I":
			if i == 0:
				return -47
			elif i == 1:
				return -60
		elif self.secondaryStructure == "T" or self.secondaryStructure == "S" or self.secondaryStructure == "C":
			return 180

	def getSideChainLowerBound(self, i):
		if self.name == "ARG" or self.name == "R":
			if i == 2: 
				return -177
			elif i == 3:
				return -167
			elif i == 4:
				return -65
			elif i == 5:
				return -175

		elif self.name == "LYS" or self.name == "K":
			if i == 2:
				return -177
			elif i == 3:
				return -68
			elif i == 4:
				return -68
			elif i == 5:
				return -65

		elif self.name == "MET" or self.name == "M":
			if i == 2:
				return -177
			elif i == 3:
				return -65
			elif i == 4:
				return -75

		elif self.name == "GLU" or self.name == "E":
			if i == 2:
				return -177
			elif i == 3:
				return -80
			elif i == 4:
				return -60
		elif self.name == "GLN" or self.name == "Q":
			if i == 2:
				return -177
			elif i == 3:
				return -75
			elif i == 4:
				return -100
		elif self.name == "ASP" or self.name == "D":
			if i == 2:
				return -177
			elif i == 3:
				return -60
		elif self.name == "ASN" or self.name == "N":
			if i == 2:
				return -177
			elif i == 3:
				return -80
		elif self.name == "ILE" or self.name == "I":
			if i == 2:
				return -177
			elif i == 3:
				return -60
		elif self.name == "LEU" or self.name == "L":
			if i == 2:
				return -177
			elif i == 3:
				return 65
		elif self.name == "HIS" or self.name == "H":
			if i == 2:
				return -177
			elif i == 3:
				return -165
		elif self.name == "TRP" or self.name == "W":
			if i == 2:
				return -177
			elif i == 3:
				return -105
		elif self.name == "TYR" or self.name == "Y":
			if i == 2:
				return -177
			elif i == 3:
				return -85
		elif self.name == "PHE" or self.name == "F":
			if i == 2:
				return -177
			elif i == 3:
				return -85
		elif self.name == "THR" or self.name == "T":
			if i == 2:
				return -177
		elif self.name == "VAL" or self.name == "V":
			if i == 2:
				return -60
		elif self.name == "SER" or self.name == "S":
			if i == 2:
				return -177
		elif self.name == "CYS" or self.name == "C":
			if i == 2:
				return -177

		print ("ERROR! Residue not Found! ", self.name)   		

	def getSideChainUpperBound(self, i):
		if self.name == "ARG" or self.name == "R":
			if i == 2: 
				return 62
			elif i == 3:
				return 180
			elif i == 4:
				return 180
			elif i == 5:
				return 180

		elif self.name == "LYS" or self.name == "K":
			if i == 2:
				return 62
			elif i == 3:
				return 180
			elif i == 4:
				return 180
			elif i == 5:
				return 180

		elif self.name == "MET" or self.name == "M":
			if i == 2:
				return 62
			elif i == 3:
				return 180
			elif i == 4:
				return 180
		elif self.name == "GLU" or self.name == "E":
			if i == 2:
				return 70 
			elif i == 3:
				return 180
			elif i == 4:
				return 60
		elif self.name == "GLN" or self.name == "Q":
			if i == 2: 
				return 70
			elif i == 3:
				return 180
			elif i == 4:
				return 100
		elif self.name == "ASP" or self.name == "D":
			if i == 2:
				return 62 
			elif i == 3:
				return 65
		elif self.name == "ASN" or self.name == "N":
			if i == 2:
				return 62
			elif i == 3:
				return 120
		elif self.name == "ILE" or self.name == "I":
			if i == 2:
				return 62
			elif i == 3:
				return 170
		elif self.name == "LEU" or self.name == "L":
			if i == 2:
				return 62
			elif i == 3:
				return 175
		elif self.name == "HIS" or self.name == "H":
			if i == 2:
				return 62.0
			elif i == 3:
				return 165.0
		elif self.name == "TRP" or self.name == "W":
			if i == 2:
				return 62
			elif i == 3:
				return 95
		elif self.name == "TYR" or self.name == "Y":
			if i == 2:
				return 62
			elif i == 3:
				return 90
		elif self.name == "PHE" or self.name == "F":
			if i == 2:
				return 62
			elif i == 3:
				return 90
		elif self.name == "THR" or self.name == "T":
			if i == 2:
				return 62
		elif self.name == "VAL" or self.name == "V":
			if i == 2:
				return 175
		elif self.name == "SER" or self.name == "S":
			if i == 2:
				return 62
		elif self.name == "CYS" or self.name == "C":
			if i == 2:
				return 62

		print ("ERROR! Residue not Found! ", self.name)

class Individual:
	aminoacids = []
	energy = 0.0
	size = 0
	indId = 0

	def __init__(self, aminoSequence):
		self.aminoacids = []
		self.energy = 0.0
		self.size = len(aminoSequence)

	def translateIndividual(self):
		translatedAngles = []
		for i in range(0, len(self.aminoacids)):
			for j in range(0, len(self.aminoacids[i].angles)):
				translatedAngles.append(self.aminoacids[i].angles[j])
		return translatedAngles

	def updateAngles(self, ang):
		index = 0

		for i in range(0,len(self.aminoacids)):
			for j in range(0, self.aminoacids[i].numAngles):
				#self.aminoacids[i].angles[j] = 0
				self.aminoacids[i].angles[j] = ang[index]
				index = index + 1

class DifferentialEvolution:
	getcontext().prec = 7
	#Common DE Parameters
	NP = 100
	F = 0.5
	CR = 1
	D = 0
	MAX = 5000
	
	#Diversification Parameters
	GAUSS = 0.0
	GAP   = 0.0

	#PSP Domain Parameters
	AMINOSEQUENCE = []
	STRUCTURESEQUENCE = []

	#Rosetta Variables
	scorefxn = 0
	generalPose = 0

	#Diversity Value
	m_nmdf = 0

	#Custom Metrics
	secondaryHit = 0
	sidechainHit = 0

	population = []
	basePopulation = []
	gapIndexes = []

	Xu=[]
	Xl=[]
	fvals=[]

	def __init__(self):
		print("Differential Evolution Instancied!")

		self.readParameters()

		pyrosetta.init()
		self.scorefxn = pyrosetta.get_fa_scorefxn()
		self.generalPose = pyrosetta.pose_from_sequence(''.join(self.AMINOSEQUENCE), "fa_standard")

		for i in range(0, self.D):
			self.Xu.insert(i, 5.12)
			self.Xl.insert(i,-5.12)

	def readParameters(self):
		with open("config.yaml", 'r') as stream:
			try:
				config = yaml.load(stream)
				self.NP = config['np']
				self.F = config['f']
				self.CR = config['cr']
				self.MAX = config['maxIteractions']
				self.GAUSS = config['gaussianFactor']
				self.GAP = config['gapPercentage']
				
				#PSP Parameters
				self.AMINOSEQUENCE = config['aminoAcidSequence']
				self.STRUCTURESEQUENCE = config['structureSequence']
				self.PROTEIN = config['proteinName']

			except yaml.YAMLError as exc:
				print(exc)

	def updateBasePopulation(self):
		for i in range (0, self.NP):
			self.basePopulation[i].updateAngles(self.population[i].translateIndividual())
			self.basePopulation[i].energy = self.population[i].energy
			self.basePopulation[i].indId = self.population[i].indId

	def printPDB(self, indiv, txtName):
		pose = self.generalPose

		for i in range(0, len(indiv.aminoacids)):
			pose.set_omega((i+1),180)
			for j in range(0, indiv.aminoacids[i].numAngles):
				if j == 0:
					pose.set_phi((i+1), indiv.aminoacids[i].angles[j])
				elif j == 1:
					pose.set_psi((i+1), indiv.aminoacids[i].angles[j])
				elif j >= 2:
					pose.set_chi((j-1), (i+1), indiv.aminoacids[i].angles[j])

		pose.dump_pdb(txtName+".pdb")

	def calculateDimensionalityProtein(self):
		dimensionality = 0
		for i in range(0, len(self.population[0].aminoacids)):
			for j in range(0, self.population[0].aminoacids[i].numAngles):
				dimensionality = dimensionality + 1
		self.D = dimensionality

	def initPopulationProtein(self):
		self.population = []
		for i in range(0,self.NP):
			amino = []
			individual = Individual(self.AMINOSEQUENCE)
			individual.indId = i
			for j in range(0, len(self.AMINOSEQUENCE)):
				amino = AminoAcid(self.AMINOSEQUENCE[j], self.STRUCTURESEQUENCE[j])
				individual.aminoacids.insert(j, copy.deepcopy(amino))
			
			individual.energy = self.funcRosetta(individual)
			self.population.insert(i, copy.deepcopy(individual))
			self.basePopulation.insert(i, copy.deepcopy(individual))

	def best1bin(self, j, trialIndividual):
		
		bestAngles = self.basePopulation[self.getBestIndividual()].translateIndividual()

		while 1:
			r1 = random.randint(0,self.NP-1)
			if r1 != j:
				break
		while 1:
			r2 = random.randint(0,self.NP-1)
			if r2 != j and r2 != r1:
				break

		jRand = random.randint(0,self.NP-1)

		trial = trialIndividual.translateIndividual()
		r1Angles = self.basePopulation[r1].translateIndividual()
		r2Angles = self.basePopulation[r2].translateIndividual()

		for d in range(0, self.D):
			if random.random() <= self.CR or d == jRand:
				trial[d] = bestAngles[d] + (Decimal(self.F)/1 * (r1Angles[d] - r2Angles[d]))

				if self.GAUSS > 0:
					trial[d] = self.gaussianMutation(trial[d], self.GAUSS)

		trialIndividual.updateAngles(trial)

		self.verifyBonds(trialIndividual, j)

		return trialIndividual.translateIndividual()

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

		trial = trialIndividual.translateIndividual()
		
		rCurr = self.basePopulation[j].translateIndividual()
		r1Angles = self.basePopulation[r1].translateIndividual()
		r2Angles = self.basePopulation[r2].translateIndividual()
		r3Angles = self.basePopulation[r3].translateIndividual()

		for d in range (0, self.D):
			if random.random() <= self.CR or d == jRand:
				#trial[d] = rCurr[d] + (Decimal(self.F)/1 * (r1Angles[d] - rCurr[d])) + (Decimal(self.F)/1 * (r2Angles[d] - r3Angles[d]))
				trial[d] = rCurr[d] + (Decimal(self.F)/1 * (r1Angles[d] - r2Angles[d]))

				if self.GAUSS > 0:
					self.gaussianMutation(trial[d], self.GAUSS)

		trialIndividual.updateAngles(trial)

		self.verifyBonds(trialIndividual, j)

		return trialIndividual.translateIndividual()

	def currToBest(self, j, trialIndividual):
		bestAngles = self.basePopulation[self.getBestIndividual()].translateIndividual()

		while 1:
			r1 = random.randint(0, self.NP-1)
			if r1 != j:
				break

		while 1:
			r2 = random.randint(0, self.NP-1)
			if r2 != r1 and r2 != j:
				break

		jRand = random.randint(0,self.NP-1)

		trial = trialIndividual.translateIndividual()
		r1Angles = self.basePopulation[r1].translateIndividual()
		r2Angles = self.basePopulation[r2].translateIndividual()

		for d in range(0, self.D):
			if random.random() <= self.CR or d == jRand:
				trial[d] = trial[d] + (Decimal(self.F)/1 * (r1Angles[d] - r2Angles[d])) + (Decimal(self.F)/1 * (bestAngles[d] - trial[d]))

				if self.GAUSS > 0:
					trial[d] = self.gaussianMutation(trial[d], self.GAUSS)

		trialIndividual.updateAngles(trial)

		self.verifyBonds(trialIndividual, j)

		return trialIndividual.translateIndividual()


	def randToBest(self, j, trialIndividual):
		bestAngles = self.basePopulation[self.getBestIndividual()].translateIndividual()

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

		trial = trialIndividual.translateIndividual()
		r1Angles = self.basePopulation[r1].translateIndividual()
		r2Angles = self.basePopulation[r2].translateIndividual()
		r3Angles = self.basePopulation[r3].translateIndividual()

		for d in range(0, self.D):
			if random.random() <= self.CR or d == jRand:
				trial[d] = r1Angles[d] + (Decimal(self.F)/1 * (r2Angles[d] - r3Angles[d])) + (Decimal(self.F)/1 * (bestAngles[d] - r1Angles[d]))
				
				if self.GAUSS > 0:
					self.gaussianMutation(trial[d], self.GAUSS)

		trialIndividual.updateAngles(trial)

		self.verifyBonds(trialIndividual, j)

		return trialIndividual.translateIndividual()

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

		trial = trialIndividual.translateIndividual()
		r1Angles = self.basePopulation[r1].translateIndividual()
		r2Angles = self.basePopulation[r2].translateIndividual()
		r3Angles = self.basePopulation[r3].translateIndividual()

		for d in range(0, self.D):						
			if random.random() <= self.CR or d == jRand:
				trial[d] = r1Angles[d] + (Decimal(self.F)/1 * (r2Angles[d] - r3Angles[d]))

				if self.GAUSS > 0:
					self.gaussianMutation(trial[d], self.GAUSS)

		trialIndividual.updateAngles(trial)
		
		self.verifyBonds(trialIndividual, j)

		return trialIndividual.translateIndividual()

	def verifyBonds(self, trialIndividual, j):
		for i in range(0, len(trialIndividual.aminoacids)):
			for k in range(0, trialIndividual.aminoacids[i].numAngles):				
				if k < 2:
					secondaryLB = trialIndividual.aminoacids[i].getSecondaryLowerBound(k)
					secondaryUP = trialIndividual.aminoacids[i].getSecondaryUpperBound(k)
						
					if trialIndividual.aminoacids[i].angles[k] < secondaryLB:
						self.secondaryHit = self.secondaryHit+1
						trialIndividual.aminoacids[i].angles[k] = Decimal(random.uniform(secondaryLB, secondaryUP))/1
					elif trialIndividual.aminoacids[i].angles[k] > secondaryUP:
						self.secondaryHit = self.secondaryHit+1
						trialIndividual.aminoacids[i].angles[k] = Decimal(random.uniform(secondaryLB, secondaryUP))/1

					if trialIndividual.aminoacids[i].angles[k] < secondaryLB:
						trialIndividual.aminoacids[i].angles[k] = self.basePopulation[j].aminoacids[i].angles[k]
					elif trialIndividual.aminoacids[i].angles[k] > secondaryUP:
						trialIndividual.aminoacids[i].angles[k] = self.basePopulation[j].aminoacids[i].angles[k]
				elif k >= 2:
					sideLB = trialIndividual.aminoacids[i].getSideChainLowerBound(k)
					sideUP = trialIndividual.aminoacids[i].getSideChainUpperBound(k)

					if trialIndividual.aminoacids[i].angles[k] > sideUP:
						self.sidechainHit = self.sidechainHit+1
						trialIndividual.aminoacids[i].angles[k] = Decimal(random.uniform(sideLB, sideUP))/1
					elif trialIndividual.aminoacids[i].angles[k] < sideLB:
						self.sidechainHit = self.sidechainHit+1
						trialIndividual.aminoacids[i].angles[k] = Decimal(random.uniform(sideLB, sideUP))/1

					if trialIndividual.aminoacids[i].angles[k] > sideUP:
						trialIndividual.aminoacids[i].angles[k] = self.basePopulation[j].aminoacids[i].angles[k]
					elif trialIndividual.aminoacids[i].angles[k] < sideLB:
						trialIndividual.aminoacids[i].angles[k] = self.basePopulation[j].aminoacids[i].angles[k]

	def getBestIndividual(self):
		bestIndex = 0
		for i in range(0, self.NP):
			if(self.basePopulation[i].energy <= self.basePopulation[bestIndex].energy):
				bestIndex = i

		return bestIndex

	def funcRosetta(self, candidate):
		pose = self.generalPose
		score = 0
		index = 0

		for i in range(0, len(candidate.aminoacids)):	
			pose.set_omega((i+1), 180)
			for j in range(0, candidate.aminoacids[i].numAngles):
				if(j==0):
					pose.set_phi((i+1), candidate.aminoacids[i].angles[j])
				elif (j == 1):
					pose.set_psi((i+1), candidate.aminoacids[i].angles[j])
				elif (j >= 2):
					pose.set_chi((j-1), (i+1), candidate.aminoacids[i].angles[j])
			
		score = self.scorefxn(pose)

		return score

	def updateDiversity(self):
		diversity = 0
		aux_1 = 0
		aux_2 = 0
		a = 0
		b = 0
		d = 0

		for a in range(0, len(self.basePopulation)):
			b = a+1
			for i in range(b, len(self.basePopulation)):
				aux_1 = 0
				
				ind_a = self.basePopulation[self.getIndexById(a)].translateIndividual()
				ind_b = self.basePopulation[self.getIndexById(b)].translateIndividual()
				
				for d in range(0, self.D):
					aux_1 = aux_1 + Decimal(pow(ind_a[d] - ind_b[d], 2).real)/1
				aux_1 = Decimal(sqrt(aux_1).real)/1
				aux_1 = Decimal(aux_1 / self.D)/1

				if b == (a+1) or aux_2 > aux_1:
					aux_2 = aux_1
			diversity = Decimal(diversity)/1 + Decimal(log(Decimal(1.0) + aux_2).real)/1

			if(self.m_nmdf < diversity):
				self.m_nmdf = diversity

			try:
				return (diversity/self.m_nmdf).real
			except (ValueError, Decimal.DecimalException):
				return 0
	
	def optimizeProtein(self):
		init_time = time.time()
		temp_time = init_time
		self.initPopulationProtein()
		self.calculateDimensionalityProtein()
		troca = []
		diversidade = []
		melhor_ind = []
		population_mean = []
		balance = 0
		strategy = 0
		i=0
		
		#Evolution Process
		for i in range(0,self.MAX):
			self.updateBasePopulation()
			
			if i % 1250 == 0:
				strategy += 1
			
			melhor_ind.append(self.basePopulation[self.getBestIndividual()].energy)
			diversidade.append(self.updateDiversity())
			
			mean = 0

			if self.GAP > 0:
				self.generationGAP()

			if i % 5 == 0:
				print("Generation: ", i, " Energy: ", melhor_ind[i], " Diversity: ", diversidade[i], " Pop Len: ", len(self.population), "Strategy: ", strategy)

			for j in range(0, len(self.population)):
				mean = mean + self.population[j].energy
				
				trial = copy.deepcopy(self.population[j])
				
				
				if strategy == 1:
					self.rand1bin(j, trial)
				elif strategy == 2:
					self.currToRand(j, trial)
				elif strategy == 3:
					self.currToRand(j, trial)
				elif strategy == 4:
					self.rand1bin(j, trial)
				
				trial.energy = self.funcRosetta(trial)

				if trial.energy <= self.population[j].energy:
					self.population[j].updateAngles(trial.translateIndividual())
					self.population[j].energy = trial.energy
			
			population_mean.insert(i, (mean/self.NP))

			if self.GAP > 0.0:
				for i in range(0, len(self.gapIndexes)):
					self.population.append(copy.deepcopy(self.basePopulation[self.getIndexById(self.gapIndexes[i])]))
		
			i += 1
		end_time = time.time()

		f = open(("execucao"+str(end_time)),'w')
		f.write("i\tenergy\tmean\tdiversity\t\n")

		for i in range(0,len(melhor_ind)):
			f.write(str(i)+"\t"+str(melhor_ind[i])+"\t"+ str(population_mean[i])+"\t"+str(diversidade[i])+"\n")
		f.close()

		f = open(("pop"+str(end_time)),'w')
		for i in range(0, self.NP):
			f.write(str(self.population[i].translateIndividual()))
			f.write("\n\n")
		f.close()

		f = open(("hits"+str(end_time)),"w")
		f.write("BackBone Failed Constrain Hit: "+str(self.secondaryHit)+"\n")
		f.write("SideChain Failed Constrain Hit: "+str(self.sidechainHit)+"\n")
		f.write("Execution Time: "+str(end_time - init_time))
		for p in range (0, len(troca)):
			f.write("\nTrocas: "+str(troca[p])+" ")
		f.close()

		self.printPDB(self.population[self.getBestIndividual()], str(end_time))

		return 0

	def funcRastring(self, trial):
		sum = 0

		for i in range(0,self.D):
			sum = sum + math.pow(trial[i],2) - 10 * math.cos (2 * math.pi * trial[i]) + 10

		return sum

	def gaussianMutation(self,value, std):
		x1 = random.random()
		x2 = random.random()

		if(x1 ==0):
			x1 = 1
		if(x2 == 0):
			x2 == 1

		y1 = Decimal(sqrt(-2.0*log(x1).real).real * cos(2.0*pi*x2).real)/1

		return Decimal((y1 * Decimal(std) + value).real)/1

	def generationGAP(self):
		perc = self.NP * self.GAP
		self.gapIndexes = []

		while len(self.gapIndexes) < int(perc):
			val = random.randint(0, len(self.population)-1)
			self.gapIndexes.append(self.population[val].indId)
			del self.population[val]

	def getIndexById(self, p_id):
		for i in range(0,self.NP):
			if self.basePopulation[i].indId == p_id:
				return i 
		return 0

	def verifyExclusion(self, rand, theList):
		for i in range(0, len(theList)):
			if rand == theList[i]:
				return True
		return False

de = DifferentialEvolution()
de.optimizeProtein()



