#Puzzles program
import random
import copy

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

class Puzzle:
	size = 0
	grid = []
	numbers = []
	moves_array = [5, 10, 15]
	directions = [['up', 'down', 'left', 'right'], ['up', 'down', 'left', 'right', 'front', 'back']]
	initial = []
	goal = []
	curstate = []

	def __init__(self, size, goal_choice, diff):
		self.size = size
		self.numbers = [i for i in range(1, size*size*size)]
		self.createGoal(goal_choice)
		self.initState(size, self.moves_array[diff - 1])

	def move(self, idx1, idx2):
		'''print("before move : ")
		print(idx1)
		print(self.curstate[self.size - idx1['z'] - 1][idx1['x']][idx1['y']])
		print(idx2)
		#print(idx2)'''
		temp = copy.deepcopy(self.curstate[self.size - idx1['z'] - 1][idx1['x']][idx1['y']])
		self.curstate[self.size - idx1['z'] - 1][idx1['x']][idx1['y']] =  copy.deepcopy(self.curstate[self.size - idx2['z'] - 1][idx2['x']][idx2['y']])
		self.curstate[self.size - idx2['z'] - 1][idx2['x']][idx2['y']] = copy.deepcopy(temp)
		#print('after move')
		#print(self.curstate[self.size - idx1['z'] - 1][idx1['x']][idx1['y']])


	def fillGrid(self):
		i = 0
		grid = []
		for z in range(self.size):
			row = []
			for x in range(self.size):
				cell = []
				for y in range(self.size):
					cell.append(self.numbers[i])
					i += 1
				row.append(cell)
			grid.append(row)

		return grid

	def createGoal(self, goal_choice):
		if goal_choice == 1: #empty in bottom-right
			self.numbers.append(0)
			self.goal = self.fillGrid()
		elif goal_choice == 2: #empty middle
			size3 = self.size**3
			self.numbers.insert(int(size3/2) , 0)
			self.goal = self.fillGrid()
		elif goal_choice == 3: #reverse order, bottom-right
			self.numbers = list(reversed(self.numbers))
			self.numbers.append(0)
			self.goal = copy.deepcopy(self.fillGrid())

	def findEmptyTile(self, state):
		for z in range(self.size):
			for x in range(self.size):
				for y in range(self.size):
					if state[z][x][y] == 0:
						#idx = {"x" : self.size - x, "y": self.size - y, "z" : self.size - z}
						idx = {"x" : x, "y": y, "z" : self.size - z - 1}
						return idx

	def initState(self, size, moves):
		i = 0	
		self.curstate = copy.deepcopy(self.goal)
		while(i < moves):
			random.shuffle(self.directions[size - 2]) #first list in directions has moves for 2D
			move = self.directions[size - 2][0]
			print(move)
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
		print("i")
		print(i)

	def PrintState(self, state):
		for z in state: #for now
			print(z)

	def testGoal(self, state):
		if self.goal == state:
			return 1;
		else:
			return 0;

	def frontierNodes(self, actions, parent, path_cost, depth):
		fn = []
		for a in actions:
			self.curstate = copy.deepcopy(parent)
			fn.append(self.createNode(parent, a, path_cost, depth))

		return fn

	def DisplacedTilesH(self, node):
		cnt = 0

		for z in range(self.size):
			for y in range(self.size):
				for x in range(self.size):
					if node.state[z][x][y] != self.goal[z][x][y]:
						cnt += 1

		return cnt

	def ManhattanDistanceH(self, node):
		md = 0
		for z in range(self.size):
			for y in range(self.size):
				for x in range(self.size):
					if node.state[z][x][y] != self.goal[z][x][y]:
						md +=  



	def BFS(self, parent):
		closed_list = []
		queue = []
		path_cost = 0

		queue.append(parent)

		while queue: #while queue not empty
			print(path_cost)
			closed_list.append(parent)
			if self.testGoal(parent.state):
				print("Goal reached by BFS")
				self.PrintState(parent.state)
				print("nodes visited")
				print(path_cost)
				return parent
			else:
				path_cost += 1 
				actions = self.frontierActions(parent.state) #generate possible actions from parent
				frontier = self.frontierNodes(actions, parent.state, path_cost, path_cost) #check parent to avoid loops
				for n in frontier:
					if n not in closed_list:
						queue.append(n)
				if queue:
					parent = copy.deepcopy(queue[0])
					queue.remove(queue[0])
		'''
		print("last parent")
		self.PrintState(parent.state)
		actions = copy.deepcopy(self.frontierActions(parent.state)) #generate possible actions from parent
		print("possible actions for last parent")
		print(actions)
		frontier = copy.deepcopy(self.frontierNodes(actions, parent.state, path_cost, path_cost)) #check parent to avoid loops
		print("possible children of last parent")
		for n in frontier:
			self.PrintState(n.state)

		print("not goal. path_cost")
		print(path_cost)'''

	def DFS(self, parent, stack, closed_list, path_cost):

		#general search algo 
		#initial state => possible actions => nodes => building tree
		#run DFS on tree => stack managing frontier => call testGoal on each node 
		#=> recursive function
		#careful with computation
		
		#assumption:
		#our algorithm works with the idea that a goal exists (existence guaranteed)
		#and is not too far off any initial state (5, 10, or 15 moves away)

		#questions:
		#path cost same as depth in DFS
		'''print("closed_list")
		for c in closed_list:
			self.PrintState(c)'''
		closed_list.append(parent);
		
		path_cost += 1
		print("cost")
		print(path_cost)
		flag = 0
		#base case 
		#print(self.testGoal(parent))
		if self.testGoal(parent.state):
			return parent

		#recursive algo
		else:
			actions = copy.deepcopy(self.frontierActions(parent.state))#generate possible actions from parent
			frontier = copy.deepcopy(self.frontierNodes(actions, parent.state, path_cost, path_cost)) #check parent to avoid loops
			print("parent: ")
			self.PrintState(parent.state)
			print("children: ")
			for n in frontier: 
				if n not in closed_list:
					flag = 1
					print(n.operator)
					self.PrintState(n.state)
					stack.append(n)
				else:
					parent.path_cost += 1
			#if parent already visited pop next
			if not stack:
				return parent
			parent = copy.deepcopy(stack.pop())
			return self.DFS(parent, stack, closed_list, path_cost)


	def frontierActions(self, state):
		idxEmpty = self.findEmptyTile(state) 
		#list of possible moves given position of empty tile
		removals = {'x0': 'left', 'x2': 'right', 'x3': 'right', 
					'y0': 'front', 'y2' : 'back', 'y3': 'back',
					'z0' : 'down', 'z2': 'up', 'z3' : 'up'}
		possibleActions  = copy.deepcopy(self.directions[self.size - 2])
		'''print("pa before")
		print(possibleActions)'''
		rmvs = [removals.get('x' + str(idxEmpty['x'])), removals.get('y' + str(idxEmpty['y'])), removals.get('z' + str(idxEmpty['z']))] 
		for elt in rmvs:
			if elt != None and elt in possibleActions: #after 'and' code meant to support 3D and 2D
				'''print("removing from pa:")
				print(elt)'''
				possibleActions.remove(elt)
		
		'''if not possibleActions:
			print("the z of the last parent")
			print(idxEmpty['z'])
			print("list of rmvs")
			print(rmvs)'''
		return possibleActions;

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


if __name__ == '__main__':

	puzzle = Puzzle(3, 3, 1);
	print('initial state')
	puzzle.PrintState(puzzle.initial)
	#print("empty tile:")
	#print(puzzle.findEmptyTile(puzzle.initial))
	print('goal state')
	puzzle.PrintState(puzzle.goal)
	#print('curstate')
	#puzzle.PrintState(puzzle.curstate)
	#print('possible actions')
	queue = []
	closed_list = []
	path_cost = 0
	node = Node(puzzle.initial, [], '', 0, 0)
	print(puzzle.DisplacedTilesH(node))
	#goal = puzzle.BFS(node)
	#dfs_goal = puzzle.DFS(node, queue, closed_list, path_cost)

	