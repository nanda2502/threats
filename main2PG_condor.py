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
from multiprocessing import Pool
import itertools

def run_simulation(args):
    
	threat, probability, replicateSim = args

	simulation_settings = {
        "seed": (threat + 1) * (probability * 100) + replicateSim,
        "GUI": False,
        "SAVEFIGS": False,
        "n": 50,  # nxn grid
        "b": 3.0,  # Contribution cost multiplication factor; called r in the paper
        "c": 1.0,  # Cost of contribution
        "lambda": 1/2.0,  # Cost of individual punishing; called lambda in the paper
        "rho": 3.0/2,  # Fine applied by individual punishment
        "basePayoff": 30,
        "infoLevel": 1,  # Probability of knowing co-player's punishment behavior
        "e": 0,  # Probability that knowledge is incorrect
        "imRate": 1,  # Immigration rate - how many immigrants to add each step
        "deathrate": 0.10,  # Probability of death
        
        "mu": 0.01,  # Exploration rate
        "neighborhood": [(-1, 0), (0, -1), (0, 1), (1, 0)],  # Agent interaction neighborhood
        "num_gens": 3000,  # Number of generations
        "types": ['C_R','C_A','C_S','C_N','D_R','D_A','D_S','D_N','Oc_R','Oc_A','Oc_S','Oc_N','Od_R','Od_A','Od_S','Od_N'],
        "contTypes": ['C','D','Oc','Od'],
        "punTypes": ['R','A','S','N'],
        "threat": threat,
        "probability": probability,
        "replicateSim": replicateSim,
    }
	simulation_settings["reproductionrate"] = 1 - simulation_settings["deathrate"]

	simulation_settings["GAMEMATRIX"] = [
        [(simulation_settings["b"] - simulation_settings["c"], simulation_settings["b"] - simulation_settings["c"]),
         (-simulation_settings["c"], simulation_settings["b"])],
        [(simulation_settings["b"], -simulation_settings["c"]), (0, 0)]
    ]
    
	# Mapping of types to integer for plotting
	simulation_settings["cTypeToInt"] = {ct: i for i, ct in enumerate(simulation_settings["contTypes"])}
	simulation_settings["pTypeToInt"] = {pt: i for i, pt in enumerate(simulation_settings["punTypes"])}
    
	simulation_settings["runId"] = f"test2PG_b{simulation_settings['b']}c{simulation_settings['c']}l{simulation_settings['lambda']}rho{simulation_settings['rho']}i{simulation_settings['infoLevel']}e{simulation_settings['e']}mu{simulation_settings['mu']}death{simulation_settings['deathrate']}im{simulation_settings['imRate']}bP{simulation_settings['basePayoff']}tau{simulation_settings['threat']}p{simulation_settings['probability']}repl{simulation_settings['replicateSim']}"

    
	rnd.seed(simulation_settings["seed"])
	
	simulation_settings["stats"] = st.Stats(
        simulation_settings['types'],
        simulation_settings['contTypes'],
        simulation_settings['punTypes'],
        simulation_settings['runId']
    )# to record statistics, e.g. counts over time

	GUI = simulation_settings["GUI"]
	n = simulation_settings["n"]
	neighborhood = simulation_settings["neighborhood"]
	num_gens = simulation_settings["num_gens"]

	if GUI:
		pycxsimulator.GUI().start(func=[lambda: init(threat, probability), draw, lambda: step(threat, probability)])
	else:
		init(n, neighborhood)
		while time < num_gens:
			step(simulation_settings)
		simulation_settings["stats"].close_files()
		print(f"Simulation {threat}, {probability}, {replicateSim} complete.")

# ~~~~~ MAIN FUNCTIONS: INIT, DRAW, STEP ~~~~~
def init(n, neighborhood):
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
	

def step(simulation_settings):
	imRate = simulation_settings["imRate"]
	types = simulation_settings["types"]
	mu = simulation_settings["mu"]
	GAMEMATRIX = simulation_settings["GAMEMATRIX"]
	l = simulation_settings["lambda"]
	rho = simulation_settings["rho"]
	infoLevel = simulation_settings["infoLevel"]
	e = simulation_settings["e"]
	reproductionrate = simulation_settings["reproductionrate"]
	threat = simulation_settings["threat"]
	probability = simulation_settings["probability"]
	basePayoff = simulation_settings["basePayoff"]
	n = simulation_settings["n"]


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
			if rnd.random() < reproductionrate:
				newAgent = makeAgentOfType(agent.agent_type)
				grid.place_agent(newAgent, rnd.choice(emptyAdjacent))
				addedAgents.append(newAgent)
	agents.extend(addedAgents)
	
	severity = threat/probability 

	##### death
	for agent in agents:
		# if the threat occurs, subtract from agent's payoff
		if rnd.random() < probability:
			deathchance = death(agent.total_payoff() + basePayoff - severity)
		else: 
			deathchance = death(agent.total_payoff() + basePayoff)
		if rnd.random() < deathchance:
			agents.remove(agent)
			grid.remove_agent(agent)

	percAlive = len(agents)/float(n*n)

	simulation_settings["stats"].step(agents, payList, coopPerc, punPerc, percAlive)	

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

def death(payoff):
	return (math.e**(-0.1*payoff))

def setContMatrix(agents, M, simulation_settings):
	for agent in agents:
		(x,y) = agent.gridlocation
		M[x][y] = simulation_settings["cTypeToInt"][agent.contributionType]

def setPunMatrix(agents, M, simulation_settings):
	for agent in agents:
		(x,y) = agent.gridlocation
		M[x][y] = simulation_settings["pTypeToInt"][agent.punishmentType]

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

if __name__ == '__main__':
	threat_values = range(0, 31, 5)
	probability_values = [0.1, 0.3, 0.5, 0.7, 0.9]
	replications = [1,2,3]
	params_list = list(itertools.product(threat_values, probability_values, replications))
	with Pool(15) as pool:
		pool.map(run_simulation, params_list)
			
