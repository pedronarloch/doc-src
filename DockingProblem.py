import random
import math
import sympy
from subprocess import getstatusoutput
from cmath import sqrt, log, cos, pi, sin
import copy
import yaml
import time
from decimal import getcontext, Decimal
from Problems import Problem
from docking import Docking
import string

class DockingProblem(Problem):

	vina_path = ''
	vina_config = ''
	docking_complex = ''
	docking = None

	cube_based_search = False

	box_bounds = []
	center_bounds = []


	def __init__(self):
		super().__init__()
		print("Docking Problem Instantied!")
		self.read_parameters()
		self.read_vina_config_file()
		self.docking = Docking(self.docking_complex, "")
		self.dimensions = 14
		self.get_bounds()

	def read_parameters(self):
		with open("docking_config.yaml", 'r') as stream:
			try:
				config = yaml.load(stream)
				self.vina_path = config['vina_path']
				self.vina_config = config['vina_config']
				self.docking_complex = config['complex']
				self.cube_based_search = config['cube_based']
			except yaml.YAMLError as exc:
				print(exc)

	def check_bounds(self, trial):

		if self.cube_based_search == True:			
			self.cube_based_bound_check(trial)

		else:			
			self.common_bound_check(trial)
			

	def cube_based_bound_check(self, trial):
		print("Cube Based Bound Check")

	def common_bound_check(self, trial):
		for i in range(0, len(trial)):
				if trial[i] < self.lb[i]:
					trial[i] = random.uniform(self.lb[i], self.ub[i])
				elif trial[i] > self.ub[i]:
					trial[i] = random.uniform(self.lb[i], self.ub[i])


	def read_vina_config_file(self):
		#print(self.docking_complex, )
		file = open("Docking/"+self.docking_complex + "/" + self.vina_config)

		while True:
			bufferLine = file.readline().split()

			if not bufferLine:
				break

			if(bufferLine[0] == "size_x"):
				self.box_bounds.append(float(bufferLine[2]))
			elif(bufferLine[0] == "size_y"):
				self.box_bounds.append(float(bufferLine[2]))
			elif(bufferLine[0] == "size_z"):
				self.box_bounds.append(float(bufferLine[2]))
			elif(bufferLine[0] == "center_x") :
				self.center_bounds.append(float(bufferLine[2]))
			elif(bufferLine[0] == "center_y"):
				self.center_bounds.append(float(bufferLine[2]))
			elif(bufferLine[0] == "center_z"):
				self.center_bounds.append(float(bufferLine[2]))


	def evaluate(self, angles):
		self.docking.performDocking(angles)
		a = getstatusoutput(self.vina_path + ' --config Docking/' + self.docking_complex +"/"+self.vina_config + ' --score_only')
		energy = (a[1].split("Affinity:")[1]).split()[0]
		return float(energy)

	def get_bounds(self, label = 0):
		self.lb.clear()
		self.ub.clear()

		if self.cube_based_search == True:			

			dimXA = (-1) * self.box_bounds[0]/2.0
			dimXB = (-1) * self.box_bounds[0]/6.0
			dimXC = self.box_bounds[0]/6.0
			dimXD = self.box_bounds[0]/2.0
			
			dimYA = (-1) * self.box_bounds[1]/2.0
			dimYB = (-1) * self.box_bounds[1]/6.0
			dimYC = self.box_bounds[1]/6.0
			dimYD = self.box_bounds[1]/2.0
			
			dimZA = (-1) * self.box_bounds[2]/2.0
			dimZB = (-1) * self.box_bounds[2]/6.0
			dimZC = self.box_bounds[2]/6.0
			dimZD = self.box_bounds[2]/2.0

			if label == 1:
				self.lb.append(dimXB, dimYB, dimZB)
				self.ub.append(dimXC, dimYC, dimZC)
			elif label == 2:
				self.lb.append(dimXB, dimYB, dimZB)
				self.ub.append(dimXA, dimYC, dimZC)
			elif label == 3:
				self.lb.append(dimXC, dimYB, dimZB)
				self.ub.append(dimXD, dimYC, dimZC)
			elif label == 4:
				self.lb.append(dimXB, dimYB, dimZB)
				self.ub.append(dimXC, dimYC, dimZA)
			elif label == 5:
				self.lb.append(dimXB, dimYB, dimZC)
				self.ub.append(dimXC, dimYB, dimZB)
			elif label == 6:
				self.lb.append(dimXC, dimYB, dimZB)
				self.ub.append(dimXD, dimXC, dimZA)
			elif label == 7:
				self.lb.append(dimXB, dimYB, dimZB)
				self.ub.append(dimXA, dimYC, dimZA)
			elif label == 8:
				self.lb.append(dimXB, dimYB, dimZC)
				self.ub.append(dimXA, dimYC, dimZD)
			elif label == 9:
				self.lb.append(dimXC, dimYB, dimZC)
				self.ub.append(dimXD, dimYC, dimZD)
			elif label == 10:
				self.lb.append(dimXB, dimYC, dimZB)
				self.ub.append(dimXC, dimYD, dimZC)
			elif label == 11:
				self.lb.append(dimXB, dimYC, dimZB)
				self.ub.append(dimXA, dimYD, dimZB)
			elif label == 12:
				self.lb.append(dimXC, dimYC, dimZB)
				self.ub.append(dimXD, dimYD, dimZC)
			elif label == 13:
				self.lb.append(dimXB, dimYC, dimZB)
				self.ub.append(dimXC, dimYD, dimZA)
			elif label == 14:
				self.lb.append(dimXB, dimYC, dimZC)
				self.ub.append(dimXC, dimYD, dimZD)
			elif label == 15:
				self.lb.append(dimXC, dimYC, dimZB)
				self.ub.append(dimXD, dimYD, dimZA)
			elif label == 16:
				self.lb.append(dimXB, dimYC, dimZB)
				self.ub.append(dimXA, dimYD, dimZA)
			elif label == 17:
				self.lb.append(dimXB, dimYC, dimZC)
				self.ub.append(dimXA, dimYD, dimZD)
			elif label == 18:
				self.lb.append(dimXC, dimYC, dimZC)
				self.ub.append(dimXD, dimYD, dimZD)
			elif label == 19:
				self.lb.append(dimXB, dimYB, dimZB)
				self.ub.append(dimXC, dimYA, dimZC)
			elif label == 20:
				self.lb.append(dimXB, dimYB, dimZB)
				self.ub.append(dimXA, dimYA, dimZC)
			elif label == 21:
				self.lb.append(dimXC, dimYB, dimZB)
				self.ub.append(dimXD, dimYA, dimZC)
			elif label == 22:
				self.lb.append(dimXB, dimYB, dimZB)
				self.ub.append(dimXC, dimYA, dimZD)
			elif label == 23:
				self.lb.append(dimXB, dimYB, dimZC)
				self.ub.append(dimXC, dimYA, dimZD)
			elif label == 24:
				self.lb.append(dimXC, dimYB, dimZB)
				self.ub.append(dimXD, dimYA, dimZA)
			elif label == 25:
				self.lb.append(dimXB, dimYB, dimZB)
				self.ub.append(dimXA, dimYA, dimZA)
			elif label == 26:
				self.lb.append(dimXB, dimYB, dimZC)
				self.ub.append(dimXA, dimYA, dimZD)
			elif label == 27:
				self.lb.append(dimXC, dimYB, dimZC)
				self.ub.append(dimXA, dimYA. dimZD)
		else:
			for i in range(0, 3):
				self.lb.append(float(self.box_bounds[i]/2) * (-1))
				self.ub.append(float(self.box_bounds[i]/2))

		for i in range(0,11):
			self.lb.append(-pi)
			self.ub.append(pi)

