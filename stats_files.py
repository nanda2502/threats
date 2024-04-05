# ##########################
#
#  *** To keep track of population statistics. ****
#   
#
# @author: roos@cs.umd.edu
# @version: aug-2013
# ##########################

import pickle as pkl
from collections import defaultdict

class Stats:

	def __init__(self, types, contTypes, punTypes, runID="x"):  # runID="x"

		self.lastPays = list()
		
		self.types = types
		self.contTypes = contTypes
		self.punTypes = punTypes

		# initialize log files
		self.contTypeFile = open("./results/contProps_"+str(runID)+".txt", 'w')
		for t in contTypes:
			if t == contTypes[-1]:
				self.contTypeFile.write(t+"\n")
			else:
				self.contTypeFile.write(t+",")

		self.punTypeFile = open("./results/punProps_"+str(runID)+".txt",'w')
		for p in punTypes:
			if p == punTypes[-1]:
				self.punTypeFile.write(p+"\n")
			else:
				self.punTypeFile.write(p+",")	

		self.allTypeFile = open("./results/allProps_"+str(runID)+".txt",'w')
		print(f"writing file {str(runID)}")
		for t in types:
			if t == types[-1]:
				self.allTypeFile.write(t+"\n")
			else:
				self.allTypeFile.write(t+",")

		self.statsFile = open("./results/stats_"+str(runID)+".txt",'w')
		self.statsFile.write("totalPopPay,coopPerc,punPerc,percAlive\n")

	def step(self, agents, payList, coopPerc, punPerc, percAlive):
		""" Records everything for this time step. """
			
		allProps, contProps, punProps = self.countPopProportions(agents)

		# proportions of contribution types
		for t in self.contTypes:
			if t == self.contTypes[-1]:
				self.contTypeFile.write(str(contProps[t])+"\n") 
			else:
				self.contTypeFile.write(str(contProps[t])+",") 

		# proportions of contribution types
		for t in self.punTypes:
			if t == self.punTypes[-1]:
				self.punTypeFile.write(str(punProps[t])+"\n") 
			else:
				self.punTypeFile.write(str(punProps[t])+",") 

		# proportions of full types
		for t in self.types:
			if t == self.types[-1]:
				self.allTypeFile.write(str(allProps[t])+"\n") 
			else:
				self.allTypeFile.write(str(allProps[t])+",") 

		#print sum(payList)
		#print("len(agents):",len(agents))
		#print("coopPerc:",coopPerc)
		#print("punPerc:",punPerc)
		self.statsFile.write(str(sum(payList))+","+str(coopPerc)+","+str(punPerc)+","+str(percAlive)+"\n")

		self.lastPays = payList		
		
	def countPopProportions(self, population):
	
		allProps = defaultdict(float)
		punProps = defaultdict(float)
		contProps = defaultdict(float)

		for a in population:
			for t in self.types:
				if a.agent_type == t:
					allProps[t] = allProps[t] + 1
			for t in self.punTypes:
				if a.punishmentType == t:
					punProps[t] = punProps[t] + 1 
			for t in self.contTypes:
				if a.contributionType == t:
					contProps[t] = contProps[t] + 1 
				
		for t in self.types:
			if len(population)>0:
				allProps[t] = float(allProps[t])/len(population)
			else:
				allProps[t] = 0				
		for t in self.punTypes:
			if len(population)>0:		
				punProps[t] = float(punProps[t])/len(population) 
			else:
				punProps[t] = 0	
		for t in self.contTypes:
			if len(population)>0:	
				contProps[t] = float(contProps[t])/len(population) 
			else:
				contProps[t] = 0
 
		return allProps, contProps, punProps

	def close_files(self):
		self.contTypeFile.close()
		self.punTypeFile.close()
		self.allTypeFile.close()
		self.statsFile.close()
