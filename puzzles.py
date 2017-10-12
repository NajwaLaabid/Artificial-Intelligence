#Puzzles program
import random

def test():
	print("hi")

class Puzzle:
	size = 0
	grid = []
	numbers = []
	moves_array = [5, 10, 15]
	initial = []
	goal = []
	actions = {'up' : 'self.moveUp'}

	def __init__(self, size, goal_choice, diff):
		self.size = size
		self.numbers = [i for i in range(1, size*size*size)]
		self.createGoal(goal_choice)
		self.initState(size, self.moves_array[diff - 1])

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

		#self.Print()
	def moveUp(self):
		print("I am up!")

	def initState(self, size, moves):
		i = 0	
		'''self.initial = self.goal
		idxTile = self.findEmptyTile()
		for i in range(moves):
			random.shuffle(directions[size - 2])
			actions[directions[size - 2][0]]()'''
		self.actions['up']()		
	
	def Print(self):
		for z in self.goal:
			print(z)

	def testGoal(self, state):
		if self.goal == state:
			return 1;
		else:
			return 0;


if __name__ == '__main__':
	puzzle = Puzzle(3, 3, 1);
	dic = {"test" : test}
	dic["test"]()
	#puzzle1 = Puzzle(3, 2, 1);
	#print(puzzle.testGoal(puzzle1.goal))
	
