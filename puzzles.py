#Puzzles program
import random
import copy

'''
- Class Node is used to generate the nodes of the search tree
- Every node has attributes as specified in the assignment
'''

class Node:
	state = []
	parent = []
	operator = ''
	path_cost = 0
	depth = 0

	def __init__(self, state, parent, operator, path_cost, depth):
		self.state = copy.deepcopy(state)
		self.parent = copy.deepcopy(parent)
		self.operator = operator
		self.path_cost = path_cost
		self.depth = depth

'''
- The Puzzle is basically the game instance
- The class provides a representation of the state of the game,
  the search strategies available, and all other auxilary functions necessary to the solving of the puzzle
'''
class Puzzle:
	#dimension of puzzle (adjusted to use in functions)
	dimension = 0

	#dimension of puzzle as specified by user
	realDimension = 0

	#directionIndx
	directionIndx = 0

	#number of tiles in each face of the puzzle
	size = 0
	
	#auxilary array used to create states
	grid = []
	
	#the numbers making up the puzzle. Auxilary array, used to generate goal state and initial state
	numbers = []
	
	#number of moves from goal to initial state
	#difficulty level determines the number of moves (5 moves for difficulty 1, 10 moves for diff. 2....)
	moves_array = [5, 10, 15]
	
	#the possible movements of a given tile
	#the first array contains the actions for the 2D grid, and the second the actions of the 3D
	directions = [['up', 'down', 'left', 'right'], ['up', 'down', 'left', 'right', 'front', 'back']]
	
	#initial state of puzzle
	initial = []

	#goal state of puzzle
	goal = []

	#current state of puzzle
	curstate = []

	#class contructor: creates goal state and initial state
	def __init__(self, size, dimension, goal_choice, difficulty):
		self.size = size 
		self.directionIndx = dimension - 2
		self.realDimension = dimension
		if dimension == 2:
			self.dimension = 1
		else:
			self.dimension = size	
		self.numbers = [i for i in range(1, size**dimension)]
		self.createGoal(goal_choice)
		self.initState(size, self.moves_array[difficulty - 1])

	#returns a goal state
	#gives choice between 3 different goals (refer to report for details)
	def createGoal(self, goal_choice):
		if goal_choice == 1: #empty in bottom-right
			self.numbers.append(0)
			self.goal = self.fillGrid()
		elif goal_choice == 2: #empty middle
			size3 = self.size**self.realDimension
			self.numbers.insert(int(size3/2) , 0)
			self.goal = self.fillGrid()
		elif goal_choice == 3: #reverse order, bottom-right
			self.numbers = list(reversed(self.numbers))
			self.numbers.append(0)
			self.goal = copy.deepcopy(self.fillGrid())

	#creates an initial state by moving the empty tile 5, 10, 
	#or 15 moves away from its goal position
	def initState(self, size, moves):
		i = 0	
		self.curstate = copy.deepcopy(self.goal)
		while(i < moves):
			random.shuffle(self.directions[self.directionIndx]) #first list in directions has moves for 2D
			move = self.directions[self.directionIndx][0]
			#move = 'up'
			idxTile = {}
			idxTile = self.findEmptyTile(self.curstate)
			if move == 'up':	
				idxTile2 = idxTile.copy()
				if idxTile2['z'] < self.size - 1: idxTile2['z'] += 1 #ignore state
				else: i -= 1
				self.move(idxTile, idxTile2)
			elif move == 'down':
				idxTile2 = idxTile.copy()
				if idxTile2['z'] > 0: idxTile2['z'] -= 1
				else: i -= 1
				self.move(idxTile, idxTile2)
			elif move == 'left':
				idxTile2 = idxTile.copy()
				if idxTile2['x'] > 0: idxTile2['x'] -= 1
				else: i -= 1
				self.move(idxTile, idxTile2)
			elif move == 'right':
				idxTile2 = idxTile.copy()
				if idxTile2['x'] < self.size - 1: idxTile2['x'] += 1
				else: i -= 1
				self.move(idxTile, idxTile2)
			elif move == 'front':
				idxTile2 = idxTile.copy()
				if idxTile2['y'] > 0: idxTile2['y'] -= 1
				else: i -= 1
				self.move(idxTile, idxTile2)
			elif move == 'back':
				idxTile2 = idxTile.copy()
				if idxTile2['y'] < self.size - 1: idxTile2['y'] += 1
				else: i -= 1
				self.move(idxTile, idxTile2)
			i += 1

		self.initial = copy.deepcopy(self.curstate)

	#tests if current state is a goal state
	def testGoal(self, state):
		if self.goal == state:
			return 1;
		else:
			return 0;

	'''Search strategies:'''

	#generic search 
	def genericSearch(self, parent, algorithm, heuristic):
		closed_list = []
		fringe = []
		nodes_visited = 0
		curPNode = (parent, 0)

		fringe.append(curPNode)
		while fringe: #while stack not empty
			total_frontier = 0
			on_fringe = 0
			curPNode = fringe[0]
			if curPNode[0].operator:
				file.write('\nAction leading to this state: ')
				file.write(" " + curPNode[0].operator)
			fringe.remove(curPNode)
			closed_list.append(curPNode[0].state)
			nodes_visited += 1

			#print progress if taking too long
			if nodes_visited % 1000 == 0:
				file.write("Search taking too long. Showing progress in every 1000 nodes...\n")
				file.write("current state\n")
				self.PrintState(curPNode[0].state)
				file.write("closed_list size:\n")
				file.write(str(len(closed_list)))
				file.write("\nfringe size:\n")
				file.write(str(len(fringe)))
				x = input("\nWould you like to continue? (Y/N)\n")
				file.write("\nWould you like to continue? (Y/N):" + x + "\n")
				if x == 'N':
					file.write("\nProgram terminated. Goal not found (yet :D)\n")
					return 0

			actions = self.frontierActions(curPNode[0].state) #generate possible actions from parent
			frontier = self.frontierNodes(actions, curPNode[0].state, curPNode[0].path_cost + 1,  curPNode[0].path_cost + 1) #check parent to avoid loops
			total_frontier += len(frontier)
			for n in frontier:
				total_frontier += 1
				if self.testGoal(n.state):
					file.write("\nAction: ")
					file.write(n.operator)
					file.write("\nGoal reached by " + algorithm + "\n")
					self.PrintState(n.state)
					file.write("\nnodes visited: ")
					file.write(str(nodes_visited))
					return n
				elif n.state not in closed_list:
					on_fringe += 1
					if algorithm == 'DFS':
						fringe = self.DFS(n, fringe)
					elif algorithm == 'BFS':
						fringe = self.BFS(n, fringe)
					elif algorithm == 'Greedy':
						fringe = self.greedyBestFirst(n, fringe, heuristic)
					elif algorithm == 'AStar':
						fringe = self.AStar(n, fringe, heuristic)
						
			file.write("\nPossible children for current node: ")
			file.write(str(total_frontier))
			file.write("\nChildren not in closed_list: ")
			file.write(str(on_fringe))
			percent_frontier_expanded = (on_fringe / total_frontier) * 100
			file.write("\nPercent of expanded nodes: ")
			file.write(str(percent_frontier_expanded) + "\n")

		return parent
	
	#uninformed search algorithms
	def BFS(self, n, fringe):
		#append in queue in fringe
		pNode = (n, 0)
		fringe.append(pNode)

		return fringe

	def DFS(self, n, fringe):
		pNode = (n, 0)
		fringe.insert(0, pNode)

		return fringe

	#Heuristics
	def DisplacedTilesH(self, node):
		cnt = 0

		for z in range(self.size):
			for x in range(self.size):
				for y in range(self.dimension):
					if node.state[z][x][y] != self.goal[z][x][y]:
						cnt += 1

		return cnt

	def ManhattanDistanceH(self, node):
		md = 0
		for z in range(self.size):
			for x in range(self.size):
				for y in range(self.dimension):
					elt = self.goal[z][x][y]
					idx1 = copy.deepcopy(self.idxEltState(node.state, elt))
					md += abs(z - idx1['z']) + abs(y - idx1['y']) + abs(x - idx1['x'])

		return md - 1

	'''	
	def patternDatabase(self, initState, ):
		for z in range(self.size)/2:
			for y in range(self.size)/2:
				for x in range(self.size)/2:'''

	#informed search alogirthms:
	def AStar(self, n, fringe, heuristic):
		if heuristic == 'MD':
			h = self.ManhattanDistanceH(n) + n.path_cost
		elif heuristic == 'DT':
			h = self.DisplacedTilesH(n) + n.path_cost

		pNode = (n, h)
		fringe = self.addToPriorityQ(fringe, pNode)

		return fringe

	def greedyBestFirst(self, n, fringe, heuristic):
		if heuristic == 'MD':
			h = self.ManhattanDistanceH(n)
		elif heuristic == 'DT':
			h = self.DisplacedTilesH(n)

		pNode = (n, h)
		fringe = self.addToPriorityQ(fringe, pNode)

		return fringe			

	'''auxilary search functions:'''

	#returns a node
	def createNode(self, parent, action, path_cost, depth):
		idx1 = self.findEmptyTile(parent)

		if action == 'up':
			idx2 = idx1.copy()
			idx2['z'] += 1
			self.move(idx1, idx2)
		elif action == 'down':
			idx2 = idx1.copy()
			idx2['z'] -= 1
			self.move(idx1, idx2)
		elif action == 'left':
			idx2 = idx1.copy()
			idx2['x'] -= 1
			self.move(idx1, idx2)
		elif action == 'right':
			idx2 = idx1.copy()
			idx2['x'] += 1
			self.move(idx1, idx2)
		elif action == 'back':
			idx2 = idx1.copy()
			idx2['y'] += 1
			self.move(idx1, idx2)
		elif action == 'front':
			idx2 = idx1.copy()
			idx2['y'] -= 1
			self.move(idx1, idx2)

		return Node(self.curstate, parent, action, path_cost, depth)

	#returns all possible next moves for a given state
	def frontierActions(self, state):
		idxEmpty = self.findEmptyTile(state) 
		#list of possible moves given position of empty tile
		removals = {'x0': 'left', 'x2': 'right', 'x3': 'right', 
					'y0': 'front', 'y2' : 'back', 'y3': 'back',
					'z0' : 'down', 'z2': 'up', 'z3' : 'up'}
		possibleActions  = copy.deepcopy(self.directions[self.directionIndx])
		rmvs = [removals.get('x' + str(idxEmpty['x'])), removals.get('y' + str(idxEmpty['y'])), removals.get('z' + str(idxEmpty['z']))] 
		for elt in rmvs:
			if elt != None and elt in possibleActions: #after 'and' code meant to support 3D and 2D
				possibleActions.remove(elt)
		return possibleActions;

	#returns all possible "children" nodes of a given parent
	#uses frontier actions returned by previous function to generate nodes
	def frontierNodes(self, actions, parent, path_cost, depth):
		fn = []
		for a in actions:
			self.curstate = copy.deepcopy(parent)
			fn.append(self.createNode(parent, a, path_cost, depth))

		return fn

	#used in AStar and Best First searches
	#adds a new node to the priorityQ depending on the value of its heuristic
	def addToPriorityQ(self, priorityQ, n):
		idx = 0
		if not priorityQ:
			idx = 1

		for p in priorityQ:
			if p[1] < n[1]:
				#print("in for loop")
				idx = priorityQ.index(p)

		if idx == 0:
			idx = len(priorityQ)
		
		priorityQ.insert(idx - 1, n) #before p

		return priorityQ

	''' general auxilary functions'''
	
	#returns the index of an empty tile 
	def findEmptyTile(self, state):
		for z in range(self.size):
			for x in range(self.size):
				for y in range(self.dimension):
					if state[z][x][y] == 0:
						idx = {"x" : x, "y": y, "z" : self.size - z - 1}
						return idx

	#returns index of an given element in a given state
	def idxEltState(self, state, elt):
		for z in range(self.size):
			for x in range(self.size):
				for y in range(self.dimension):
					if state[z][x][y] == elt:
						#no need to adjust z cause only used to get difference
						idx = {'z': z, 'y': y, 'x': x} 
						return idx

	#used to swap two tiles (make a move)
	def move(self, idx1, idx2):
		temp = copy.deepcopy(self.curstate[self.size - idx1['z'] - 1][idx1['x']][idx1['y']])
		self.curstate[self.size - idx1['z'] - 1][idx1['x']][idx1['y']] =  copy.deepcopy(self.curstate[self.size - idx2['z'] - 1][idx2['x']][idx2['y']])
		self.curstate[self.size - idx2['z'] - 1][idx2['x']][idx2['y']] = copy.deepcopy(temp)

	#create grid from array of numbers
	def fillGrid(self):
		i = 0
		grid = []
		for z in range(self.size):
			row = []
			for x in range(self.size):
				cell = []
				for y in range(0, self.dimension):
					cell.append(self.numbers[i])
					i += 1
				row.append(cell)
			grid.append(row)

		return grid

	#prints a given state
	def PrintState(self, state):
		for z in state: #for now
			file.write(str(z))
			file.write("\n")

if __name__ == '__main__':

	print("*********** Menu ****************")
	print("Please choose your settings: ")
	dimension = int(input("Dimension (2 or 3): "))
	size = int(input("Size (3 or 4): "))
	goal = int(input("Goal choice (1, 2 or 3): "))
	difficulty = int(input("Difficulty level (1, 2 or 3): "))
	algorithm = input("Algorithm to use for search (BFS, DFS, AStar, Greedy): ")

	file = open("Greedy4.txt", "w")

	file.write("Dimension (2 or 3):" + str(dimension) + "\n")
	file.write("Size (3 or 4):" + str(size) + "\n")
	file.write("Goal choice (1, 2 or 3):" + str(goal) + "\n")
	file.write("Difficulty level (1, 2 or 3):" + str(difficulty) + "\n")
	file.write("Algorithm to use for search (BFS, DFS, AStar, Greedy):" + algorithm + "\n")
	
	puzzle = Puzzle(size, dimension, goal, difficulty);
	file.write("\n This is your goal state:\n")
	puzzle.PrintState(puzzle.goal)
	file.write("This is your initial state:\n")
	puzzle.PrintState(puzzle.initial)

	parent = []
	operator = ''
	node = Node(puzzle.initial, parent, operator, 0, 0)

	heuristic = " "

	if algorithm == "AStar" or algorithm == "Greedy":
		heuristic = input("Input heuristic (MD for Manhattan Distance, DT for Displaced Tiles): ")
		file.write("Input heuristic (MD for Manhattan Distance, DT for Displaced Tiles):" + heuristic + "\n")

	file.write("Searching...\n\n")
	puzzle.genericSearch(node, algorithm, heuristic)
