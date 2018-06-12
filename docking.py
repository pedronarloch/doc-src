from atom import *
from complexAtoms import *
import copy
import math
import numpy as np
import os
import string
import time
import sys

class Docking:
	pdbPattern = "{:6s}{:5d}  {:^4s}{:4s}{:2s}{:1s}{:1s}{:8.3f}{:8.3f}{:8.3f}{:6.2f}{:7.2f}{:10.3f}{:<4s}"
	indexRef = 0
	indexSec = 0
	branchs = {}
	indexBranch = {}
	startBranchs = {}
	endBranchs = {}
	numBranchs = 0
	receptorPath = ''
	ATOM_TAG = ["HETATM", "ATOM"]
	BRANCH_TAG = "BRANCH"
	ENDBRANCH_TAG = "ENDBRANCH"
	END_TAG = "TORSDOF"
	posAtoms = []
	modPosAtoms = []
	content = []
	atomRef = None
	atomSec = None
	indexTranslate = {}

	def __init__( self, receptor, run ):
		self.posAtoms = []
		self.content = []
		self.branchs = {}
		self.indexBranch = {}
		self.startBranchs = {}
		self.endBranchs = {}
		self.indexTranslate = {}
		self.originalPath = "./Docking/" + receptor + "/original/ligand.pdbqt"
		self.receptorPath = "./Docking/" + receptor + "/modified/ligand.pdbqt"
		#complexTag = receptor.split( "/" )[1] + "/" + receptor.split( "/" )[2]
		self.atomRef, self.atomSec = getAtomsByComplex( receptor )
		self.readFile()

		print(self.originalPath)
		
		if run == "server":
			self.receptorPath = "./Docking/" + receptor + '/modified' + os.environ['SGE_TASK_ID'] + '/ligand.pdbqt'

		elif run == "azure":
			self.receptorPath = "./Docking/" + receptor + '/modified' + os.environ['AZURE_TASK_ID'] + '/ligand.pdbqt'

	# read original file of ligand to get base informations
	def readFile( self ):
		finish = False
		file = open( self.originalPath, "r" )
		countStartBranchs = 1
		countEndBranchs = 1

		while not finish:
			line = file.readline()

			if not line:
				finish = True

			else:
				atom = Atom( line )
				self.content.append( atom )				

				if atom.getTag() == self.END_TAG:
					finish = True

				else:
					if ( atom.getTag() in self.ATOM_TAG ):						
						self.posAtoms.append( atom.getPos() )
						
						# get central atom's index (reference to bigger cube)
						if atom.getAtom() == self.atomRef:
							self.indexRef = len( self.posAtoms ) - 1

						elif atom.getAtom() == self.atomSec:
							self.indexSec = len( self.posAtoms ) - 1

						self.indexTranslate[atom.getSerial()] = len( self.posAtoms )

					# get ligand branchs (ligand's rotation points)
					elif atom.getTag() == self.BRANCH_TAG:
						branch = line.split()
						self.branchs[countStartBranchs] = ( int( branch[1] ), int( branch[2] ) )
						self.startBranchs[countStartBranchs] = len( self.posAtoms )
						self.indexBranch[branch[1] + branch[2]] = countStartBranchs
						countStartBranchs += 1

					elif atom.getTag() == self.ENDBRANCH_TAG:
						branch = line.split()
						self.endBranchs[self.indexBranch[branch[1] + branch[2]]] = len( self.posAtoms ) - 1

		file.close()
		self.numBranchs = len( self.indexBranch )
		#print self.branchs

	# get the real position of an atom
	def translatePosition( self, index ):
		return self.indexTranslate.get( index )

	# multiply two matrix
	def multiplyMatrix( self, matrixA, matrixB ):		
		linesA = len( matrixA )
		columnsA = len( matrixA[0] )
		linesB = len( matrixB )
		columnsB = len( matrixB[0] )

		if columnsA == linesB:
			dimension = columnsA
			matrixResult = [[sum( matrixA[m][n] * matrixB[n][p] for n in range( dimension ) ) \
			for p in range( columnsB )] for m in range( linesA )]
			return matrixResult

		else:
			return -1

	# translate matrix with 2 origin points (old and new)
	def translateToRef( self, matrix, reference, origin ):
		translation = origin - reference
		translation = np.array( [translation] * len( matrix ) )
		return matrix + translation

	# normalize vector
	def normalize( self, vector ):
		norm = np.linalg.norm( vector )
		if norm == 0: 
			return vector

		return vector/norm

	# rotate structure in function by angle
	def rotateMatrixTheta( self, theta, vectorReference, matrix ):
		vector = copy.copy( vectorReference )
		vector = self.normalize( vector )
		cosValue = math.cos( theta )
		sinValue = math.sin( theta )
		tValue = 1.0 - cosValue
		x = vector[0]
		y = vector[1]
		z = vector[2]

		rotationMatrix = np.array( [[( tValue * x * x ) + cosValue, ( tValue * x * y ) - ( sinValue * z ), ( tValue * x * z ) + ( sinValue * y )],
						  [( tValue * x * y ) + ( sinValue * z ), ( tValue * y * y ) + cosValue, ( tValue * y * z - ( sinValue * x ) )],
						  [( tValue * x * z ) - ( sinValue * y ), ( tValue * y * z ) + ( sinValue * x ), ( tValue * z * z ) + cosValue]] )
		#print "mRotacao", rotationMatrix
		for i in range(len( matrix )):
			#print [matrix[i][0]], [matrix[i][1]], [matrix[i][2]]
			result = self.multiplyMatrix( rotationMatrix, [[matrix[i][0]], [matrix[i][1]], [matrix[i][2]]] )
			matrix[i][0] = result[0][0]
			matrix[i][1] = result[1][0]
			matrix[i][2] = result[2][0]

		return matrix

	# rotate atoms in function of dihedral angles
	def rotateDihedralAngles( self, theta ):
		phi = 0
		psi = 0
		omega = 0
		for key in self.startBranchs.keys():
			vecRef = np.array( [list(map(float,self.modPosAtoms[self.translatePosition( self.branchs[key][0] ) -1]))[0] - list(map(float,self.modPosAtoms[self.translatePosition( self.branchs[key][1] ) -1]))[0],
					  			list(map(float,self.modPosAtoms[self.translatePosition( self.branchs[key][0] ) -1]))[1] - list(map(float,self.modPosAtoms[self.translatePosition( self.branchs[key][1] ) -1]))[1],
					  			list(map(float,self.modPosAtoms[self.translatePosition( self.branchs[key][0] ) -1]))[2] - list(map(float,self.modPosAtoms[self.translatePosition( self.branchs[key][1] ) -1]))[2]] )

			angle = theta[key - 1]
			reference = self.modPosAtoms[self.translatePosition( self.branchs[key][0] ) - 1]

			for i in range( self.startBranchs[key], self.endBranchs[key] + 1 ):
				self.modPosAtoms[i] = self.translateToRef( self.modPosAtoms[i], reference, ( 0.0, 0.0, 0.0 ) )[0]				
				self.modPosAtoms[i] = self.rotateMatrixTheta( angle, vecRef, [self.modPosAtoms[i]] )[0]
				self.modPosAtoms[i] = self.translateToRef( self.modPosAtoms[i], ( 0.0, 0.0, 0.0 ), reference )[0]

			#print self.modPosAtoms

	# rotate matrix by theta angle
	def rotateMatrix( self, angle ):
		oldOrigin = self.modPosAtoms[self.indexRef]
		#print oldOrigin
		self.modPosAtoms = self.translateToRef( self.modPosAtoms, self.modPosAtoms[self.indexRef], ( 0.0, 0.0, 0.0 ) )
		vectorRef = [ self.modPosAtoms[self.indexRef][0] - self.modPosAtoms[self.indexSec][0],
					  self.modPosAtoms[self.indexRef][1] - self.modPosAtoms[self.indexSec][1],
					  self.modPosAtoms[self.indexRef][2] - self.modPosAtoms[self.indexSec][2] ]
		
		#print self.modPosAtoms
		#print "vref", vectorRef
		self.modPosAtoms = self.rotateMatrixTheta( angle, vectorRef, self.modPosAtoms )
		#print self.modPosAtoms
		self.modPosAtoms = self.translateToRef( self.modPosAtoms, self.modPosAtoms[self.indexRef], oldOrigin )

	# translate matrix by x, y, z values
	def translateMatrix( self, translation ):
		translation = np.array( [translation] * len( self.posAtoms ) )
		self.modPosAtoms = self.modPosAtoms + translation

	# perform docking of ligand based in translation and rotation of its structure and in the internal rotation of dihedral angles
	def performDocking( self, individual ):
		self.modPosAtoms = np.array( copy.copy( self.posAtoms ) )
		# rotate dihedral angles
		self.rotateDihedralAngles(individual[4:])
		# rotate structure
		self.rotateMatrix( individual[3] )
		# translate structure
		self.translateMatrix( [individual[0], individual[1], individual[2]] )
		# write PDB with new atom positions
		self.writeLigand()

	# write content of ligand
	def writeLigand( self ):
		pdbNew = open( self.receptorPath, "w" )
		countTotal = 1

		for key in range( 0, len( self.content ) ):
			if ( self.content[key].getTag() in self.ATOM_TAG ):
				pdbNew.write( self.pdbPattern.format( self.content[key].tag, self.content[key].getSerial(), self.content[key].getAtom(), self.content[key].locIndicator, self.content[key].residue, self.content[key].chainID, \
							  self.content[key].seqResidue, float( self.modPosAtoms[countTotal - 1][0] ), float( self.modPosAtoms[countTotal - 1][1] ), float( self.modPosAtoms[countTotal - 1][2] ), \
							  float( self.content[key].occupancy ), float( self.content[key].temperature ), float( self.content[key].symbol ), self.content[key].chargeAtom ) )

				countTotal += 1
			else:
				pdbNew.write( str( self.content[key].getContent() ) )

		pdbNew.close()
