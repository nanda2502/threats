# #############################
#
# Torus class to facilitate a grid environment on which agents interact.
#
# @author: roos@cs.umd.edu	
# #############################

class Torus:
	"""
	Torus class to facilitate a grid environment on which agents interact.
	"""
	def __init__(self, nrows, ncols, neighborhood):
		self.nrows, self.ncols = nrows, ncols
		self.neighborhood = neighborhood # list of tuples of x,y-offsets (relative to any grid location).
		self.agentMatrix = [[None]*ncols for i in range(nrows)] # ncols x nrows matrix that has agent or None at each location
		
		self.emptySites = [(i,j) for i in range(nrows) for j in range(ncols)]

		self.neighborLocs = {} # for each location (x,y) key will hold neighboring locations as list
		for i in range(self.nrows):
			for j in range(self.ncols):
				neighLocs = list()
				for offset in self.neighborhood:
					dc, dr = offset		 #note: x,y neighborhood
					r = (i + dr) % nrows
					c = (j + dc) % ncols
					neighLocs.append((r,c))
				self.neighborLocs[(i,j)] = neighLocs
	
		#print "neighLocs.keys():", self.neighborLocs.keys()

	def place_agent(self, agent, loc):
		"""
		Places agent on grid at (x,y).
		"""
		x = loc[0]
		y = loc[1]
		agent.gridlocation = (x,y)
		self.agentMatrix[x][y] = agent
		self.emptySites.remove((x,y))

	def remove_agent(self, agent):
		""" Removes agent from grid. """
		self.agentMatrix[agent.gridlocation[0]][agent.gridlocation[1]] = None
		self.emptySites.append(agent.gridlocation)

	def move_agent(self, agent, loc):
		""" Moves agent to loc. """
		self.agentMatrix[agent.gridlocation[0]][agent.gridlocation[1]] = None
		self.emptySites.append(agent.gridlocation)		
		
		self.agentMatrix[loc[0]][loc[1]] = agent
		self.emptySites.remove(loc)
		agent.gridlocation = loc
		
	def switch_agents(self, agent1, agent2):
		""" Switches locations of agent1 and agent2. """
		self.agentMatrix[agent1.gridlocation[0]][agent1.gridlocation[1]] = agent2
		self.agentMatrix[agent2.gridlocation[0]][agent2.gridlocation[1]] = agent1

		temploc = agent1.gridlocation
		agent1.gridlocation = agent2.gridlocation
		agent2.gridlocation = temploc
	
	def get_all_neigh_agent_pairs(self):
		""" Returns list of all pairs of neighboring locations that have agents in them. """
	
		pairs = set()
		for origLoc in self.neighborLocs.keys():
			if self.agentMatrix[origLoc[0]][origLoc[1]] != None: # there is an agent here
				for loc in self.neighborLocs[origLoc]:
					if self.agentMatrix[loc[0]][loc[1]] != None: # there is an agent at this neighboring loc
						pairs.add((self.agentMatrix[origLoc[0]][origLoc[1]],self.agentMatrix[loc[0]][loc[1]]))

		return list(pairs)

	def get_empty_sites(self):
		"""
		Returns list of (x,y) tuples that are empty grid locations.
		"""
		return self.emptySites

	def get_neighbors(self, agent):
		"""
		Return neighbors of agent.
		"""

		#agent_row, agent_col = agent.gridlocation
		neighbors = list()
		neighlocs = self.neighborLocs[agent.gridlocation]
		for loc in neighlocs:
			if self.agentMatrix[loc[0]][loc[1]] != None:
				neighbors.append(self.agentMatrix[loc[0]][loc[1]])

		#nrows, ncols = grid.nrows, grid.ncols
		#agents2d = grid.agents2d

		# initialize list of neighbors
		#neighbors = list()

		# append all neighbors to list
		#for offset in self.neighborhood:
		#	dc, dr = offset		 #note: x,y neighborhood
		#	r = (agent_row + dr) % nrows
		#	c = (agent_col + dc) % ncols
		#	neighbor = agents2d[r][c]
		#	neighbors.append(neighbor)

		return neighbors

	def place_all(self, agentsList):
		"""
		Fills grid with agents, in sequential order at (0,0), (0,1) ... (n,n).
		Assumes len(agents) is enough for every grid location.
		"""

		agents = iter(agentsList)
		# put a agent in each grid location (row, column)
		for row in range(self.nrows):
			for column in range(self.ncols):
				agent = agents.next()
				self.agentMatrix[row][column] = agent
				agent.gridlocation = (row, column)
				self.emptySites.remove((row, column))
	
	def get_average_number_of_neighbors(self):
			total_neighbors = 0
			agent_count = 0

			for i in range(self.nrows):
				for j in range(self.ncols):
					agent = self.agentMatrix[i][j]
					if agent is not None:
						agent_count += 1
						neighbors = self.get_neighbors(agent)
						total_neighbors += len(neighbors)

			if agent_count == 0:
				return 0  # Avoid division by zero if there are no agents.

			average_neighbors = total_neighbors / agent_count
			return average_neighbors
				

