# 
# Simulator for evolutionary PGG games with punishment and reputation (?)
#
# author: roos
# edited by: lucas molleman
# jan-2014

import random as rnd
import math
import sys
import pickle
from collections import defaultdict
import PGG_players
import public_goods_game
import stats_files as st
from torus import *
from two_player_game import *
#sys.path.append("./networkx-1.7/")
#import networkx as nx
rnd.seed()


GUI = False 
SAVEFIGS = False 


################################# World Parameters ###################################
n = 50 # grid is nxn

b = 3.0 #float(sys.argv[2]) #3.5			# contribution cost multiplication factor; in the paper called r
c = 1.0			# cost of contribution
l = 1/2.0		# cost of individual punishing; called lambda in the paper
rho = 3.0/2		# fine applied by individual punishment

GAMEMATRIX = [ [(b-c,b-c),(-c,b)] , [(b,-c),(0,0)] ]
#GAMEMATRIX = [ [(2,2),(0,1)] , [(1,0),(1,1)] ]

threat = float(sys.argv[1])
probability = float(sys.argv[2]) 
replicateSim = float(sys.argv[3])
basePayoff = threat/probability
print(basePayoff)
infoLevel = 1 #0.7#1#0.6#"auto" # probability of knowing co-player's punishment behavior
e = 0 #0.05# 0.05#0.10 #05		# probability that knowledge is incorrect

imRate = 1		# immigration rate - how many immigrants to add each step
deathrate = 0.10 # probability of death

mu = 0.01		# exploration rate

neighborhood = [(-1,0),		# agents will interact with others in this neighborhood of x, y offsets
				(0,-1),
				(0,+1),
				(+1,0)]

### number of generations
num_gens = 3000 

# agent types used in population
types = ['C_R','C_A','C_S','C_N','D_R','D_A','D_S','D_N','Oc_R','Oc_A','Oc_S','Oc_N','Od_R','Od_A','Od_S','Od_N']
contTypes = ['C','D','Oc','Od']
punTypes = ['R','A','S','N']

# dictionaries to map types to integer, for plotting
cTypeToInt = {}
for i in range(len(contTypes)):
	cTypeToInt[contTypes[i]] = i
pTypeToInt = {}
for i in range(len(punTypes)):
	pTypeToInt[punTypes[i]] = i

runId = "test2PG_b" + str(b) + "c" + str(c) + "l" + str(l)+"rho"+str(rho)+"i"+str(infoLevel)+"e"+str(e)+"mu"+str(mu) + \
		"death" + str(deathrate) + "im" + str(imRate) + "bP" + str(30) + "t" + str(threat) + "p" + str(probability) + "repl"+ str(replicateSim) # str(sys.argv[2]

#runId = "2PG+_staghunt"+str(l)+"rho"+str(rho)+"i"+str(infoLevel)+"e"+str(e)+"mu"+str(mu)+"death"+str(deathrate)+"im"+str(imRate) \
#			+"bP"+str(basePayoff)+"t"+str(threat)+str(sys.argv[2])

stats = st.Stats(types, contTypes, punTypes, runId) # to record statistics, e.g. counts over time


# ~~~~~ MAIN FUNCTIONS: INIT, DRAW, STEP ~~~~~
def init():
	"""
	Creates and initializes agents and grid.
	"""

	global time, agents, grid
	time = 0

	# number of all agent types
	#numCR =	numCA = numCS = numCN = numDR = numDA = numDS = numDN = numOcR = numOcA = numOcS = numOcN = numOdR = numOdA = numOdS = numOdN = 00
	#numOdN = n*n

	# make list of agents
	#agents = makePopulation(numCR, numCA, numCS, numCN, numDR, numDA, numDS, numDN, numOcR, numOcA, numOcS, numOcN, numOdR, numOdA, numOdS, numOdN)
	agents = []

	#place all agents grid
	grid = Torus(n, n, neighborhood)
	

def step():
	"""
	Steps through time period stages by Hammond and Axelrod (2006):
	- immigration, interaction, reproduction, death.
	"""

	global time, agents, grid	

	for agent in agents:
		agent.reset()

	##### immigration --- place immigrants with random traits on random site.
	emptySites = grid.get_empty_sites()
	randEmptySitesToPopulate = rnd.sample(emptySites,min(imRate,len(emptySites)))
	for loc in randEmptySitesToPopulate: 
		immigrant = spawnRandomAgent(types)
		grid.place_agent(immigrant, loc)
		agents.append(immigrant)

	#mutation
	mutatedAgents = list()
	for agent in agents:
		if rnd.random() < mu:
			loc = agent.gridlocation
			mutant = spawnRandomAgent(types)
			agents.remove(agent)
			grid.remove_agent(agent)
			grid.place_agent(mutant, loc)
			mutatedAgents.append(mutant)
	agents.extend(mutatedAgents)	

	
	coopPercs = list()
	punPercs = list()
	####################### game phase
	# each agent plays public goods games with all neighbors and gets payoffs, punishment also included
	for agent in agents:
		#print agent.gridlocation
		players = grid.get_neighbors(agent)
		players.append(agent)

		for player in players:
			if player not in agent.players_played():
				game = TwoPlayerGame(agent, player, GAMEMATRIX, l, rho, infoLevel, e)
				CPerc, punPerc = game.run()
				coopPercs.append(CPerc)
				punPercs.append(punPerc)

	if len(coopPercs) > 0:
		coopPerc = sum(coopPercs)/float(len(coopPercs))
		punPerc = sum(punPercs)/float(len(punPercs))
	else:
		coopPerc = punPerc = 0

	payList = list()
	for agent in agents:
		payList.append(agent.total_payoff())

	##### reproduction - agents with empty adjacent spot get fitness chance to reproduce
	rnd.shuffle(agents)
	addedAgents = list()
	for agent in agents:
		# give agent chance (ptr) to clone into a random open adjacent spot, if it exists
		emptyAdjacent = [loc for loc in grid.neighborLocs[agent.gridlocation] if grid.agentMatrix[loc[0]][loc[1]] == None]
		if emptyAdjacent:
			if rnd.random() < probability:
				cost = threat/probability
			else:
				cost = 0
			if rnd.random() < fitness(agent.total_payoff() + basePayoff - cost):
				print(fitness(agent.total_payoff() + basePayoff - cost))
				newAgent = makeAgentOfType(agent.agent_type)
				grid.place_agent(newAgent, rnd.choice(emptyAdjacent))
				addedAgents.append(newAgent)
	agents.extend(addedAgents)
	
	##### death
	for agent in agents:
		if rnd.random() < deathrate:
			agents.remove(agent)
			grid.remove_agent(agent)


	percAlive = len(agents)/float(n*n)

	stats.step(agents, payList, coopPerc, punPerc, percAlive)	

	##### mobility
	#if mobility:
	#	for agent in agents:
	#		if rnd.random() < mobility:
				# move to random open spot 
	#			moveToLoc = rnd.choice(grid.emptySites)
	#			grid.move_agent(agent, moveToLoc)

	time += 1
	
def sigmoidFitness(payoff):
	#return (1.0 + math.e**(-5.0 *((payoff-threat)/12 - 0.5)))**-1
	return (1.0 + math.e**(-8.0 *((payoff)/22 - 0.5)))**-1

def fitness(payoff):
	return (1.0 - math.e**(-0.1*payoff))

def setContMatrix(agents, M):
	for agent in agents:
		(x,y) = agent.gridlocation
		M[x][y] = cTypeToInt[agent.contributionType]

def setPunMatrix(agents, M):
	for agent in agents:
		(x,y) = agent.gridlocation
		M[x][y] = pTypeToInt[agent.punishmentType]

def setPayMatrix(agents, M):
	for agent in agents:
		(x,y) = agent.gridlocation
		M[x][y] = agent.total_payoff()

def examples():

	r = 3
	c = 1
	l = 1.0/2
	rho = 3.0/2
	infoProb = 0.5

	# run one game
	players = list()
	players.append(PGG_players.CR_Agent())
	players.append(PGG_players.DR_Agent())
	players.append(PGG_players.DR_Agent())
	players.append(PGG_players.CR_Agent())
	players.append(PGG_players.CR_Agent())

	PGG = public_goods_game.PublicGoodsGame(players, r, c, l, rho, infoProb)
	print("contribution phase...")
	PGG.runContributionPhase()
	for a in players:
		print(a.agent_type, "payoff:", a.total_payoff())
	print("punishment phase...")
	PGG.runPunishmentPhase()
	for a in players:
		print(a.agent_type, "payoff:", a.total_payoff())

	# run one game
	players = list()
	players.append(PGG_players.CR_Agent())
	players.append(PGG_players.DN_Agent())
	players.append(PGG_players.DN_Agent())
	players.append(PGG_players.CR_Agent())
	players.append(PGG_players.CR_Agent())

	print("round one....")
	PGG = public_goods_game.PublicGoodsGame(players, r, c, l, rho, infoProb)
	print("contribution phase...")
	PGG.runContributionPhase()
	for a in players:
		print(a.agent_type, "payoff:", a.total_payoff()	)
	print("punishment phase...")
	PGG.runPunishmentPhase()
	for a in players:
		print(a.agent_type, "payoff:", a.total_payoff()	)

	print("round two....")
	PGG = public_goods_game.PublicGoodsGame(players, r, c, l, rho, infoProb)
	print("contribution phase...")
	PGG.runContributionPhase()
	for a in players:
		print(a.agent_type, "payoff:", a.total_payoff())
	print("punishment phase...")
	PGG.runPunishmentPhase()
	for a in players:
		print(a.agent_type, "payoff:", a.total_payoff())

	# run one game
	players = list()
	players.append(PGG_players.OcR_Agent())
	players.append(PGG_players.DN_Agent())
	players.append(PGG_players.DN_Agent())
	players.append(PGG_players.OcR_Agent())
	players.append(PGG_players.OcR_Agent())

	PGG = public_goods_game.PublicGoodsGame(players, r, c, l, rho, infoProb)
	print("contribution phase...")
	PGG.runContributionPhase()
	for a in players:
		print(a.agent_type, "payoff:", a.total_payoff())
	print("punishment phase...")
	PGG.runPunishmentPhase()
	for a in players:
		print(a.agent_type, "payoff:", a.total_payoff())

def registerCmap(count):
	""" Create a colormap with N (N<=15)discrete colors and register it. """
	# define individual colors as hex values
	cpool = [ '#0000CD', '#FF0000', '#7B68EE', '#9370DB',]
	mycmap = mpl.colors.ListedColormap(cpool[0:count], 'ContTypes')
	mycmap.set_bad('w',1.)
	mpl.cm.register_cmap(cmap=mycmap)

	cpool = ['#00FF7F', '#FF1493', '#C71585', '#CCFFFF']
	mycmap = mpl.colors.ListedColormap(cpool, 'PunTypes')
	mycmap.set_bad('w',1.)
	mpl.cm.register_cmap(cmap=mycmap)


def makePopulation(numCR, numCA, numCS, numCN, numDR, numDA, numDS, numDN, numOcR, numOcA, numOcS, numOcN, numOdR, numOdA, numOdS, numOdN):
	"""
	Returns a population that is a list of agents with counts given by parameters.
	"""

	population=list()
	for i in range(0,numCR):
		population.append(PGG_players.CR_Agent())
	for i in range(0,numCA):
		population.append(PGG_players.CA_Agent())
	for i in range(0,numCS):
		population.append(PGG_players.CS_Agent())
	for i in range(0,numCN):
		population.append(PGG_players.CN_Agent())
	for i in range(0,numDR):
		population.append(PGG_players.DR_Agent())
	for i in range(0,numDA):
		population.append(PGG_players.DA_Agent())
	for i in range(0,numDS):
		population.append(PGG_players.DS_Agent())
	for i in range(0,numDN):
		population.append(PGG_players.DN_Agent())
	for i in range(0,numOcR):
		population.append(PGG_players.OcR_Agent())
	for i in range(0,numOcA):
		population.append(PGG_players.OcA_Agent())
	for i in range(0,numOcS):
		population.append(PGG_players.OcS_Agent())
	for i in range(0,numOcN):
		population.append(PGG_players.OcN_Agent())
	for i in range(0,numOdR):
		population.append(PGG_players.OdR_Agent())
	for i in range(0,numOdA):
		population.append(PGG_players.OdA_Agent())
	for i in range(0,numOdS):
		population.append(PGG_players.OdS_Agent())
	for i in range(0,numOdN):
		population.append(PGG_players.OdN_Agent())
		
	return population

def spawnRandomAgent(types):
	return makeAgentOfType(rnd.choice(types))	

def makeAgentOfType(agentType):
	
	if agentType == "C_R":
		return PGG_players.CR_Agent()
	elif agentType == "C_A":
		return PGG_players.CA_Agent()
	elif agentType == "C_S":
		return PGG_players.CS_Agent()
	elif agentType == "C_N":
		return PGG_players.CN_Agent()
	elif agentType == "D_R":
		return PGG_players.DR_Agent()
	elif agentType == "D_A":
		return PGG_players.DA_Agent()
	elif agentType == "D_S":
		return PGG_players.DS_Agent()
	elif agentType == "D_N":
		return PGG_players.DN_Agent()
	elif agentType == "Oc_R":
		return PGG_players.OcR_Agent()
	elif agentType == "Oc_A":
		return PGG_players.OcA_Agent()
	elif agentType == "Oc_S":
		return PGG_players.OcS_Agent()
	elif agentType == "Oc_N":
		return PGG_players.OcN_Agent()
	elif agentType == "Od_R":
		return PGG_players.OdR_Agent()
	elif agentType == "Od_A":
		return PGG_players.OdA_Agent()
	elif agentType == "Od_S":
		return PGG_players.OdS_Agent()
	elif agentType == "Od_N":
		return PGG_players.OdN_Agent()

########################################################################################################

# for running simulation using pyxcsimulator

if __name__ == "__main__":
	if GUI:
		pycxsimulator.GUI().start(func=[init,draw,step])
	else:
		init()
		while time < num_gens:
			step()
		stats.close_files()
		print(f"Finished {threat} {probability} {replicateSim}.")
		
			

