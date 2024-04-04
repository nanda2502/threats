## 
##
##
## author: Patrick Roos (roos@cs.umd.edu)

class PublicGoodsGame:
 

	def __init__(self, playerlist, r, c, l, rho, infoProb, e, 
			punTypes = ['R','A','S','N'] ):
		
		self.players = playerlist
		self.r = r
		self.c = c
		self.l = l
		self.rho = rho
		self.infoProb = infoProb
		self.e = e
		self.punTypes = punTypes

		self.payoffs = {} # to hold payoff assignments from this game {player -> payoff} 

		# history will be a list of moves made in game
		self.history = list()

	def getOpponents(self,player):
		return [a for a in  self.players if a != player]

	def run(self):
		"""
		runs contribution and punishment phase and returns cooperation %. 
		"""
		percCs = self.runContributionPhase()
		percPuns = self.runPunishmentPhase()
		# prompt players to record the game played (i.e., 'self')
		for a in self.players:
			a.record(self)

		return percCs, percPuns

	def runContributionPhase(self):
	

		#print "game:"
		#for p in self.players:
		#	print p.agent_type
			
		for a in self.players:
			a.record(self)
	
		# get moves and append these to history
		moves = [a.contributionMove(self) for a in self.players]
		self.history.append(moves)
		#print "moves:"
		#print moves

		# calculate and assign all payoffs from contribution phase
		numCs = len([m for m in moves if m =='C']) 
		totalContributions = numCs * self.c
		totalBenefit = totalContributions * self.r
		b_each = totalBenefit/float(len(self.players)) # benefit to each player from contributions

		for a in self.players:
			# add benefit to each from contributions			
			self.payoffs[a] = b_each
			# subtract contribution cost if player contributed
			if moves[self.players.index(a)] == 'C':		
				self.payoffs[a] = self.payoffs[a] - self.c
			
		return numCs/float(len(moves))
				
	def runPunishmentPhase(self):
		
		moves = self.history[-1]
		numPuns=0
		punOpps=0
		# each player has chance to punish all opponents
		for a in self.players:
			for opp in self.getOpponents(a):
				punOpps +=1
				decidedToPunish = a.punishMove(self, opp) 
				if decidedToPunish:
					self.payoffs[a] = self.payoffs[a] - self.l
					self.payoffs[opp] = self.payoffs[opp] - self.rho
					numPuns +=1

		return numPuns/float(punOpps)

	def payoff(self):
		""" Returns dictionary {player -> payoff from game}."""
		return self.payoffs

	def get_last_move(self, player):
		# if history not empty, return prior move of `player`
		if self.history:
			player_idx = self.players.index(player)
			last_move = self.history[-1][player_idx]
		else:
			last_move = None
			
		return last_move
	
				 
			
