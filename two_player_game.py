# ###############################
# 
# *** class to play a two player game ***
# 
#
# @author: roos@cs.umd.edu
# ###############################


class TwoPlayerGame:
	def __init__(self, player1, player2, payoffmat, l, rho, infoProb, e):
		
		self.players = [ player1, player2 ]
		self.payoffmat = payoffmat
		self.opponents = {player1:player2, player2:player1}
		self.c = self.payoffmat[0][0]
		self.infoProb = infoProb
		self.e = e
		self.l = l
		self.rho = rho

		self.payoffs = {} # to hold payoff assignments from this game {player -> payoff} 

		# history will be a list of moves for each iteration ((p1_move, p2_move), (p1move, p2_move), ...)
		self.history = list() 
		
		
	def run(self):
		
		player1, player2 = self.players
	
		#print "---\ngame"
		#print "player1:",player1.agent_type
		#print "player2:",player2.agent_type

		numCs = 0
		numMoves = 0
		# each iteration, get new moves and append these to history
		newmoves = player1.contributionMove(self), player2.contributionMove(self)
		moves = list()
		for m in newmoves:
			numMoves +=1
			if m == 'C':
				numCs +=1
				moves.append(m)
			else:
				moves.append(m)
		self.history.append(moves)
		
		#print "moves:", moves

		#translate player 0 and player 1's move to payoff index ('C' = 0, 'D' = 1)
		if moves[0] == 'C':
			move0 = 0
		else:
			move0 = 1
		if moves[1] == 'C':
			move1 = 0
		else:
			move1 = 1

		payoffs = self.payoffmat[move0][move1]

		self.payoffs[player1] = payoffs[0]
		self.payoffs[player2] = payoffs[1]

		#print "payoffs before pun:",payoffs

		numPuns=0
		punOpps=0
		# each player has chance to punish all opponents
		for a in self.players:
			opp = self.opponents[a]
			punOpps +=1
			decidedToPunish = a.punishMove(self, opp) 
			#print a,"deciding to punish..."
			#print "opponents last move:",self.get_last_move(opp)
			if decidedToPunish:
				#print "decided to punish!!"
				self.payoffs[a] = self.payoffs[a] - self.l
				self.payoffs[opp] = self.payoffs[opp] - self.rho
				numPuns +=1

		#print "payoffs after pun:",self.payoffs

		# prompt players to record the game played (i.e., 'self')
		player1.record(self); player2.record(self)

		#print "payoffs after pun:",player1.total_payoff(), player2.total_payoff()

		return numCs/float(numMoves), numPuns/float(punOpps)

	def getOpponents(self, agent):
		return [self.opponents[agent]]

	def payoff(self):
		return self.payoffs

	"""
	def get_payoffs(self):
		# unpack the two players
		player1, player2 = self.players
		# generate a payoff pair for each game iteration in history
		payoffs = (self.payoffmat[m1][m2] for (m1,m2) in self.history)
		# transpose to get a payoff sequence for each player
		pay1, pay2 = transpose(payoffs)
		# return a mapping of each player to its mean payoff
		return { player1:mean(pay1), player2:mean(pay2) }
	"""

	def get_last_move(self, player):
		# if history not empty, return prior move of `player`
		if self.history:
			player_idx = self.players.index(player)
			last_move = self.history[-1][player_idx]
		else:
			last_move = None
			
		return last_move
	
	def get_coops_defects(self, player):
		defects = 0
		coops = 0
		playerIndex = self.players.index(player)
		for moves in self.history:	
			if moves[playerIndex] == 0:
				coops+=1
			else:	
				defects +=1
		
		return (coops,defects)
			
