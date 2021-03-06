#!/usr/bin/env python
#Import
import os
import time
import random
from move_arm import *
from board_finder.msg import TicTacToe
import os
from threading import *


game = None


#Print the header
def print_header():
	print"""
 _____  _  ____     _____  ____  ____     _____  ____  _____
/__ __\/ \/   _\   /__ __\/  _ \/   _\   /__ __\/  _ \/  __/    1 | 2 | 3
  / \  | ||  / _____ / \  | / \||  / _____ / \  | / \||  \      4 | 5 | 6
  | |  | ||  \_\____\| |  | |-|||  \_\____\| |  | \_/||  /_     7 | 8 | 9
  \_/  \_/\____/     \_/  \_/ \|\____/     \_/  \____/\____\
                                                            
 To play Tic-Tac-Toe, you need to get three in a row...
 Your choices are defined, they must be from 1 to 9...

"""

lock = Lock()

#Each instance represents a single game of tic tac toe
class TTTGame:
	board = None 
	x = None
	y = None
	z = None
	turn = None
	first = None
	robot = None
	human = None
	init = False
	xCount = 0
	oCount = 0
	
	
	def __init__(self):
		self.board = ["", " ", " ", " ", " ", " ", " ", " ", " ", " "]
		self.armMover = ArmMover()
		#set the first to go and robot shape
		#don't pick move until we have a game board in vision
		#use vision callback to decide move
		first = 0
		self.armMover.move_arm_default('l')
		self.armMover.move_arm_default('r')

		#who goes first?
		while(first != 1 and first != 2):
			first = raw_input("Who goes first? (1 = Computer, 2 = Human) ")
			
			try:
				first = int(first)
			except:
				continue

			if first == 1:
				self.robot = "O"
				self.first = self.robot
				self.human = "X"
				#self.turn = self.robot
			elif first == 2:
				self.robot = "X"
				self.human = "O"
				self.first = self.human
				#self.turn = self.human
			else:
				print 'you must input 1 for computer or 2 for human'
		print 'init game'
		self.init = True
			

	def newGamePrompt(self):
		new_game = ''
		while(new_game != 'y' and new_game != 'n'):
			new_game = raw_input("Would you like to play again? (y or n) ")
		return new_game
		
	
	#updates board state with vision board state
	#determines if there is a winner or the game is a tie
	#figures out whose turn it is
	def updateBoard(self, visionBoard, x, y, z):
		
		index = 1
		#update board
		for space in visionBoard:
			if(space == 0):
				self.board[index] = " "
			elif(space == 1):
				self.board[index] = "O"
			elif(space == 2):
				self.board[index] = "X"
			else:
				print ('bad value in board')
	
			index += 1

		self.x = x
		self.y = y
		self.z = z

		if(self.is_board_full()):
			print "tie game"
			return 1

		if(self.is_winner(self.robot)):
			print self.robot+" wins the game"
			self.board = ["", " ", " ", " ", " ", " ", " ", " ", " ", " "]
			return 1

		if(self.is_winner(self.human)):
			print self.human+" wins the game"
			self.board = ["", " ", " ", " ", " ", " ", " ", " ", " ", " "]
			return 1

		self.whoseTurn()
		
		return 0

	#figure out whose move it is based on number of X's or O's
	def whoseTurn(self):
		countX = 0
		countO = 0
		for space in self.board:
			if(space == "O"):
				countO += 1
			elif(space == "X"):
				countX += 1
			
		#print countO, countX
		if(countO == countX):
			if(self.turn != self.first):
				self.turn = self.first
				if(self.turn == self.robot):
					choice = self.get_computer_move(self.board, self.robot, self.human)[0]
					self.robotMove(choice)
				else:
					self.humanMove()
			
					
		elif(countO > countX):
			if(self.turn == "O"):
				if(self.turn == self.robot):
					self.turn = self.human
					self.humanMove()
				else:
					self.turn = self.robot
					choice = self.get_computer_move(self.board, self.robot, self.human)[0]
					self.robotMove(choice)
		
		else:
			if(self.turn == "X"):
				if(self.turn == self.robot):
					self.turn = self.human
					self.humanMove()
				else:
					self.turn = self.robot
					choice = self.get_computer_move(self.board, self.robot, self.human)[0]
					self.robotMove(choice)
				
		

	#moves the arm to the specified square on the board
	def robotMove(self, choice):
		#make robot move to coordinates based on choice
		print 'robot chose '+str(choice)
		choice -= 1
		if(self.y[choice] >= 0):
			arm = 'l'
		else:
			arm = 'r'

		'''
		if(choice == 7):
			arm = 'r'
		elif(choice == 9):
			arm = 'l'
		'''

		#move arm to an intermediate waypoint 30 cm above chosen point
		self.armMover.move_arm(self.x[choice]-.17, self.y[choice], self.z[choice]+.38, 1.0, arm)

		#move arm to 8 cm above the chosen square position
		self.armMover.move_arm(self.x[choice]-.17, self.y[choice], self.z[choice]+.08, 1.0, arm)

		#make model appear, this should be substitued for stamping the spot
		#or dropping a token, or drawing a symbol in future
		self.spawnModel(self.robot, self.x[choice], self.y[choice], self.z[choice])

		#move arm back to default position		
		self.armMover.move_arm_default(arm, self.x[choice]-.17, self.y[choice], self.z[choice]+.08)


	def clearBoard(self):
		self.board = ["", " ", " ", " ", " ", " ", " ", " ", " ", " "]
		for i in range(0, self.xCount):
			self.deleteModel("X"+str(i))
		for i in range(0, self.oCount):
			self.deleteModel("O"+str(i))
	
	#delete a model from gazebo
	def deleteModel(self, name):
		command = "rosservice call gazebo/delete_model '{model_name: "+name+"}'"
		os.system(command)


	#Define the print_board function 
	def print_board(self):
		print "   |   |   "
		print " "+self.board[1]+" | "+self.board[2]+" | "+self.board[3]+"  "
		print "   |   |   "
		print "---|---|---"
		print "   |   |   "
		print " "+self.board[4]+" | "+self.board[5]+" | "+self.board[6]+"  "
		print "   |   |   "
		print "---|---|---"
		print "   |   |   "			
		print " "+self.board[7]+" | "+self.board[8]+" | "+self.board[9]+"  "
		print "   |   |   "
	

	def is_winner(self, player, board = None):
		if(board == None):
			board = self.board

		if (board[1] == player and board[2] == player and board[3] == player) or \
			(board[4] == player and board[5] == player and board[6] == player) or \
			(board[7] == player and board[8] == player and board[9] == player) or \
			(board[1] == player and board[4] == player and board[7] == player) or \
			(board[2] == player and board[5] == player and board[8] == player) or \
			(board[3] == player and board[6] == player and board[9] == player) or \
			(board[1] == player and board[5] == player and board[9] == player) or \
			(board[3] == player and board[5] == player and board[7] == player):
			return True
		else:
			return False
		
	#tie game
	def is_board_full(self, board = None):
		if board == None:
			board = self.board
		if " " in board:
			return False
		else:
			return True
			
			
	#human inputs space to place symbol. Must be available space between
	#1 and 9
	def humanMove(self):
		print 'human move'
		choice = 0
		while(self.board[choice] != " "):
			choice = raw_input("Please choose an empty space for "+self.human+" ")
			try:
				choice = int(choice)
			except:
				choice = 0
				continue

			if(choice < 1 or choice > 9):
				choice = 0

			if self.board[choice] == " ":
				choice -= 1
				self.spawnModel(self.human, self.x[choice], self.y[choice], self.z[choice])
				break
			else:
				print "Sorry, that space is not empty!"
				time.sleep(1)
		
		#automatically make piece appear in specified choice in gazebo
		
		
	#Minimax algorithm for robot to pick optimal 
	def get_computer_move(self, board, shape, otherShape):
	
		index = 0
		bestMove = None
		for space in board:
		
			if(space == ' '):
				tempBoard = board[:]
				tempBoard[index] = shape
				if(self.is_winner(shape, tempBoard)):
					return (index, -10)
			
				elif(self.is_board_full(tempBoard)):
					return (index, 0)
				
				else:
					move = self.get_computer_move(tempBoard, otherShape, shape)
					if(bestMove == None):
						bestMove = (index, move[1])
					else:
						if(move[1] > bestMove[1]):
							bestMove = (index, move[1])
				
			index += 1
		return (bestMove[0], -bestMove[1])


		#count is the index of this model, because the naming must be unique
	def spawnModel(self,piece, x, y, z):
	
		#print os.getcwd()
		path_to_models = os.getcwd()+"/src/system_launch/models/"
		model = ""
		if (piece == "X"):
			model = "X.urdf"
			count = self.xCount
			self.xCount += 1
		elif(piece == "O"):
			model = "O.urdf"
  			count = self.oCount
			self.oCount += 1
		else:
			print 'bad piece sent to spawn model'
			return

		count = piece+str(count)
		coords = " -x " + str(x) +  " -y " + str(y) + " -z " + str(z)	
		command = "rosrun gazebo_ros spawn_model -file " + path_to_models + model + " -urdf -model " + str(count) + coords
		#don't forget to #import os
		os.system(command)


#received message from vision callback
def callback(msg):
	global game
	
	#get rid of any message that has been held in a queue for longer than 200 ms
	if(abs(rospy.get_time() - (msg.header.stamp.secs + msg.header.stamp.nsecs / 100000000.0 + .200)) > 0.200):
		return
		

	if(game == None):
		return

	#don't care about board until the game is started
	if(game.init == False):
		return

	result = game.updateBoard(msg.state, msg.x, msg.y, msg.z)
	#game ended condition
	if(result == 1):
		game.init = False
		newGame = game.newGamePrompt()
		if(newGame == 'y'):
			game.clearBoard()
			game = TTTGame()
		else:
			game.clearBoard()
			rospy.signal_shutdown("Game Over")



if __name__ == '__main__':
	rospy.init_node('game')
	rospy.Subscriber("board_finder/TicTacToe", TicTacToe, callback, queue_size=2)
	global game
	game = TTTGame()
	print("Starting game node")
	rospy.spin()



	
	
	
