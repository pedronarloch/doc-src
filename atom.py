# Read the PDBQT's content and split values in variables to better access

class Atom( object ):
	tag = ''
	serial = ''
	atom = ''
	locIndicator = ''
	residue = ''
	chainID = ''
	seqResidue = ''
	insResidue = ''
	xCor = ''
	yCor = ''
	zCor = ''
	occupancy = ''
	temperature = ''
	symbol = ''
	chargeAtom = ''
	line = ''
	bFrom = '' 
	bTo = ''
	ATOM_TAG = ["HETATM", "ATOM"]
	BRANCH_TAG = "BRANCH"
	ENDBRANCH_TAG = "ENDBRANCH"

	def __init__( self, line ):
		if line[0:6].strip() in self.ATOM_TAG:
			self.tag = line[0:6]
			self.serial = line[6:13]
			self.atom = line[13:17]
			self.locIndicator = line[17:21]
			self.residue = line[21:23]
			self.chainID = line[23:26]
			self.seqResidue = line[26:30]
			self.insResidue = line[30:31]
			self.xCor = line[31:39]
			self.yCor = line[39:47]
			self.zCor = line[47:55]
			self.occupancy = line[55:61]
			self.temperature = line[61:67]
			self.symbol = line[67:76]
			self.chargeAtom = line[76:80]

		elif line[0:6] == self.BRANCH_TAG:
			self.tag = line[0:6]
			self.bFrom = line[6:11]
			self.bTo = line[11:15]

		elif line[0:9] == self.ENDBRANCH_TAG:
			self.tag = line[0:9]
			self.bFrom = line[9:13]
			self.bTo = line[13:17]

		self.line = line

	def getTag( self ):
		return self.tag.strip()

	def getSerial( self ):
		return int( self.serial.strip() )

	def getAtom( self ):
		return self.atom.strip()

	def getResidue( self ):
		return self.residue.strip()

	def getPos( self ):
		return [float(self.xCor), float(self.yCor), float(self.zCor)]

	def getContent( self ):
		return self.line