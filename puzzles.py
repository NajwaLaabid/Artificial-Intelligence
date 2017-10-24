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
		self.state  = state
		self.parent = parent
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
		temp = self.curstate[idx1['z']][idx1['x']][idx1['y']] 
		self.curstate[idx1['z']][idx1['x']][idx1['y']] =  self.curstate[idx2['z']][idx2['x']][idx2['y']] 
		self.curstate[idx2['z']][idx2['x']][idx2['y']] = temp

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
			self.goal = self.fillGrid()

	def findEmptyTile(self, state):
		for z in range(self.size):
			for x in range(self.size):
				for y in range(self.size):
					if state[z][x][y] == 0:
						idx = {"x" : x, "y": y, "z" : z}
						return idx

	def initState(self, size, moves):
		i = 0	
		self.curstate = copy.deepcopy(self.goal)
		while(i < moves):
			random.shuffle(self.directions[size - 2]) #first list in directions has moves for 2D
			move = self.directions[size - 2][0]
			idxTile = {}
			idxTile = self.findEmptyTile(self.curstate)
			if move == 'up':
				idxTile2 = idxTile.copy()
				if idxTile2['z'] > 0: idxTile2['z'] -= 1 #ignore state
				else: i -= 1
				self.move(idxTile, idxTile2)
			elif move == 'down':
				idxTile2 = idxTile.copy()
				if idxTile2['z'] < 2: idxTile2['z'] += 1
				else: i -= 1
				self.move(idxTile, idxTile2)
			elif move == 'left':
				idxTile2 = idxTile.copy()
				if idxTile2['x'] > 0: idxTile2['x'] -= 1
				else: i -= 1
				self.move(idxTile, idxTile2)
			elif move == 'right':
				idxTile2 = idxTile.copy()
				if idxTile2['x'] < 2: idxTile2['x'] += 1
				else: i -= 1
				self.move(idxTile, idxTile2)
			elif move == 'front':
				idxTile2 = idxTile.copy()
				if idxTile2['y'] > 0: idxTile2['y'] -= 1
				else: i -= 1
				self.move(idxTile, idxTile2)
			elif move == 'back':
				idxTile2 = idxTile.copy()
				if idxTile2['y'] < 2: idxTile2['y'] += 1
				else: i -= 1
				self.move(idxTile, idxTile2)
			i += 1

		self.initial = copy.deepcopy(self.curstate)

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
			fn.append(self.createNode(parent, a, path_cost, depth))

		return fn

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
		closed_list.append(parent);
		path_cost += 1
		flag = 0
		#base case 
		if self.testGoal(parent) == 1:
			return parent;

		#recursive algo
		else:
			actions = self.frontierActions(parent) #generate possible actions from parent
			frontier = self.frontierNodes(actions, parent, path_cost, path_cost) #check parent to avoid loops
			for n in frontier: 
				if n not in closed_list:
					flag = 1
					stack.append(n)
			if flag:
				path_cost = 1
			#if parent already visited pop next
			parent = stack.pop()
			self.DFS(parent.state, stack, closed_list, path_cost)


	def frontierActions(self, state):
		idxEmpty = self.findEmptyTile(state) 
		#list of possible moves given position of empty tile
		removals = {'x0': 'left', 'x2': 'right', 'x3': 'right', 
					'y0': 'front', 'y2' : 'back', 'y3': 'back',
					'z0' : 'down', 'z2': 'up', 'z3' : 'up'}
		possibleActions  = self.directions[self.size - 2]
		rmvs = [removals.get('x' + str(idxEmpty['x'])), removals.get('y' + str(idxEmpty['y'])), removals.get('z' + str(idxEmpty['z']))] 
		for elt in rmvs:
			if elt != None and elt in possibleActions: #after 'and' code meant to support 3D and 2D
				possibleActions.remove(elt)
	
		return possibleActions;

	def createNode(self, parent, action, path_cost, depth):
		idx1 = self.findEmptyTile(parent)
		#generate state using move function
		self.curstate = parent
		if action == 'up':
			idx2 = {'x' : idx1['x'], 'y': idx1['y'], 'z' : idx1['z'] + 1}
			self.move(idx1, idx2)
		elif action == 'down':
			idx2 = {'x' : idx1['x'], 'y': idx1['y'], 'z' : idx1['z'] - 1}
			self.move(idx1, idx2)
		elif action == 'left':
			idx2 = {'x' : idx1['x'] - 1, 'y': idx1['y'], 'z' : idx1['z']}
			self.move(idx1, idx2)
		elif action == 'right':
			idx2 = {'x' : idx1['x'] + 1, 'y': idx1['y'], 'z' : idx1['z']}
			self.move(idx1, idx2)
		elif action == 'back':
			idx2 = {'x' : idx1['x'], 'y': idx1['y'] + 1, 'z' : idx1['z']}
			self.move(idx1, idx2)
		elif action == 'front':
			idx2 = {'x' : idx1['x'], 'y': idx1['y'] - 1, 'z' : idx1['z']}
			self.move(idx1, idx2)

		#generate node and return it 
		return Node(self.curstate, parent, action, path_cost, depth)


if __name__ == '__main__':
	puzzle = Puzzle(3, 2, 2);
	print('initial state')
	puzzle.PrintState(puzzle.initial)
	print('possible actions')
	stack = []
	closed_list = []
	path_cost = 0
	print(puzzle.DFS(puzzle.initial, stack, closed_list, path_cost))
	