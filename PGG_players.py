#
# Player Classes for the PG game.
#
# author: roos
# aug-2012
import random

class BasicAgent(object):

	def __init__(self, agent_type, gridloc = None):
		self.agent_type = agent_type
		self.gridlocation = gridloc
		self.reset()     # sets self.games_played to empty list

	def getFitness(self, w=0.99):
		return (1 - w + w*self.total_payoff())

	def record(self, game):
		"""
		Records the game played to history (games_played).
		"""
		self.games_played.append(game)

	def reset(self):
		"""
		Resets history to empty.
		"""
		self.games_played = list()  

	def total_payoff(self):
		"""
		Returns total payoff received from all games recorded.
		"""
		return sum( game.payoff()[self] for game in self.games_played )

	def avg_payoff(self):

		return sum( game.payoff()[self] for game in self.games_played )/float(len(self.games_played))

	def players_played(self):
		players = list()
		for game in self.games_played:
			players.append(game.opponents[self])
		return players

####################### Conribution Phase Types #########################
class Cooperator(object):
	"""
	Cooperators always contribute to the public good. 
	"""
	def contributionMove(self, game):
		return 'C'
		
class Defector(object):
	"""
	Defectors never contribute to the public good. 
	"""
	def contributionMove(self, game):
		return 'D'

class OpportunisticCooperator(object):
	"""
	Contribute, unless they know that it is beneficial to defect (which is the case if they know
	that the number of social sanctioners R in the group is below or equal to the number of
	antisocial punishers A).
	"""

	def contributionMove(self, game):
		
		if random.random() < game.infoProb:
			# reputation of all co-players known			
			opponents = game.getOpponents(self)
	
			# with prob game.e, the type of opponent is observed as a different random type
			observedPunTypes = list()
			for opp in opponents:
				if random.random() < game.e:
					observedPunTypes.append(random.choice([t for t in game.punTypes if t != opp.punishmentType]))
				else:	
					observedPunTypes.append(opp.punishmentType)

			numR = len([t for t in observedPunTypes if t == 'R'])
			numA = len([t for t in observedPunTypes if t == 'A'])
			
			if game.c[0]/game.rho < (numR/float(len(opponents)) - numA/float(len(opponents))) * len(opponents):
				return 'C'
			else:
				return 'D'
		else:
			# no reputation known, default to C
			return 'C'

class OpportunisticDefector(object):
	"""
	Defect, unless they know that it is beneficial to cooperate (which is the case if they know
	that the number of social sanctioners R in the group exceeds the number of
	antisocial punishers A).
	"""

	def contributionMove(self, game):
		
		if random.random() < game.infoProb:
			# reputation of all co-players known			
			opponents = game.getOpponents(self)

			# with prob game.e, the type of opponent is observed as a different random type
			observedPunTypes = list()
			for opp in opponents:
				if random.random() < game.e:
					observedPunTypes.append(random.choice([t for t in game.punTypes if t != opp.punishmentType]))
				else:	
					observedPunTypes.append(opp.punishmentType)

			numR = len([t for t in observedPunTypes if t == 'R'])
			numA = len([t for t in observedPunTypes if t == 'A'])
			#numR = len([opp for opp in opponents if opp.punishmentType == 'R'])
			#numA = len([opp for opp in opponents if opp.punishmentType == 'A'])
			
			#if game.c[0]/game.rho < numR/float(len(opponents)) - numA/float(len(opponents)):
			#if game.c[0]/game.rho < (numR/float(len(opponents)) - numA/float(len(opponents))) * len(opponents):
			if 1.0/game.rho < (numR/float(len(opponents)) - numA/float(len(opponents))) * len(opponents):
				return 'C'
			else:
				return 'D'

			#if numR == numA:
			#	return 'D'
			#elif numR > numA:
			#	return 'C'
			#else:
			#	return 'D'

		else:
			# no reputation known, default to D
			return 'D'


####################### Punishment Phase Types #########################
class ResponsibleSanctioner(object):
	"""
	Punishes Defectors only.
	"""

	def punishMove(self, game, agent):
		if game.get_last_move(agent) == 'D':
			return True 
		else:
			return False

class AntiSocialSanctioner(object):
	"""
	Punishes Cooperators only.
	"""

	def punishMove(self, game, agent):
		if game.get_last_move(agent) == 'C':
			return True
		else:
			return False

class SpitefullSanctioner(object):
	"""
	Punishes errrbody.
	"""

	def punishMove(self, game, agent):
		return True

class NonSanctioner(object):
	"""
	Punishes nobody.
	"""

	def punishMove(self, game, agent):
		return False


######################### FULL PLAYER TYPES (16 total) #######################
# inherit both punishment phase type and contribution phase type

class CR_Agent(BasicAgent, Cooperator, ResponsibleSanctioner):

	def __init__(self):
		super(CR_Agent, self).__init__("C_R")		
		self.punishmentType = 'R'
		self.contributionType = 'C'
		
	def makeOffspring(self):
		return CR_Agent()
		

class CA_Agent(BasicAgent, Cooperator, AntiSocialSanctioner):

	def __init__(self):
		super(CA_Agent, self).__init__("C_A")
		self.punishmentType = 'A'
		self.contributionType = 'C'
		
	def makeOffspring(self):
		return CA_Agent()		

class CS_Agent(BasicAgent, Cooperator, SpitefullSanctioner):

	def __init__(self):
		super(CS_Agent, self).__init__("C_S")
		self.punishmentType = 'S'
		self.contributionType = 'C'
	
	def makeOffspring(self):
		return CS_Agent()

class CN_Agent(BasicAgent, Cooperator, NonSanctioner):

	def __init__(self):
		super(CN_Agent, self).__init__("C_N")
		self.punishmentType = 'N'
		self.contributionType = 'C'
		
	def makeOffspring(self):
		return CN_Agent()

class DR_Agent(BasicAgent, Defector, ResponsibleSanctioner):

	def __init__(self):
		super(DR_Agent, self).__init__("D_R")
		self.punishmentType = 'R'
		self.contributionType = 'D'
		
	def makeOffspring(self):
		return DR_Agent()

class DA_Agent(BasicAgent, Defector, AntiSocialSanctioner):

	def __init__(self):
		super(DA_Agent, self).__init__("D_A")
		self.punishmentType = 'A'
		self.contributionType = 'D'
		
	def makeOffspring(self):
		return DA_Agent()

class DS_Agent(BasicAgent, Defector, SpitefullSanctioner):

	def __init__(self):
		super(DS_Agent, self).__init__("D_S")
		self.punishmentType = 'S'
		self.contributionType = 'D'

		
	def makeOffspring(self):
		return DS_Agent()

class DN_Agent(BasicAgent, Defector, NonSanctioner):

	def __init__(self):
		super(DN_Agent, self).__init__("D_N")
		self.punishmentType = 'N'
		self.contributionType = 'D'
		
	def makeOffspring(self):
		return DN_Agent()

class OcR_Agent(BasicAgent, OpportunisticCooperator, ResponsibleSanctioner):

	def __init__(self):
		super(OcR_Agent, self).__init__("Oc_R")
		self.punishmentType = 'R'
		self.contributionType = 'Oc'
		
	def makeOffspring(self):
		return OcR_Agent()

class OcA_Agent(BasicAgent, OpportunisticCooperator, AntiSocialSanctioner):

	def __init__(self):
		super(OcA_Agent, self).__init__("Oc_A")
		self.punishmentType = 'A'
		self.contributionType = 'Oc'
		
	def makeOffspring(self):
		return OcA_Agent()

class OcS_Agent(BasicAgent, OpportunisticCooperator, SpitefullSanctioner):

	def __init__(self):
		super(OcS_Agent, self).__init__("Oc_S")
		self.punishmentType = 'S'
		self.contributionType = 'Oc'
		
	def makeOffspring(self):
		return OcS_Agent()

class OcN_Agent(BasicAgent, OpportunisticCooperator, NonSanctioner):

	def __init__(self):
		super(OcN_Agent, self).__init__("Oc_N")
		self.punishmentType = 'N'
		self.contributionType = 'Oc'
		
	def makeOffspring(self):
		return OcN_Agent()

class OdR_Agent(BasicAgent, OpportunisticDefector, ResponsibleSanctioner):

	def __init__(self):
		super(OdR_Agent, self).__init__("Od_R")
		self.punishmentType = 'R'
		self.contributionType = 'Od'

	def makeOffspring(self):
		return OdR_Agent()

class OdA_Agent(BasicAgent, OpportunisticDefector, AntiSocialSanctioner):

	def __init__(self):
		super(OdA_Agent, self).__init__("Od_A")
		self.punishmentType = 'A'
		self.contributionType = 'Od'
		
	def makeOffspring(self):
		return OdA_Agent()

class OdS_Agent(BasicAgent, OpportunisticDefector, SpitefullSanctioner):

	def __init__(self):
		super(OdS_Agent, self).__init__("Od_S")		
		self.punishmentType = 'S'
		self.contributionType = 'Od'
		
	def makeOffspring(self):
		return OdS_Agent()

class OdN_Agent(BasicAgent, OpportunisticDefector, NonSanctioner):

	def __init__(self):
		super(OdN_Agent, self).__init__("Od_N")
		self.punishmentType = 'N'
		self.contributionType = 'Od'
		
	def makeOffspring(self):
		return OdN_Agent()
