#!/usr/bin/env python
#Import
import os
import time
import random
from move_arm import *
from board_finder.msg import TicTacToe

game = None
#Define the board
#board = ["", " ", " ", " ", " ", " ", " ", " ", " ", " "]

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

def move_arm_default():
	move_arm(.30, .5, 1, 1,'l')
	move_arm(.30, -.5, 1, 1,'r')


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
	
	
	def __init__(self):
		self.board = ["", " ", " ", " ", " ", " ", " ", " ", " ", " "]
		#set the first to go and robot shape
		#don't pick move until we have a game board in vision
		#use vision callback to decide move
		first = 0
		move_arm_default()
		while(first != 1 and first != 2):
			first = raw_input("Who goes first? (1 = Computer, 2 = Human) ")
			first = int(first)
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
			
	
	def updateBoard(self, visionBoard, x, y, z):

		index = 1
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
			return 1

		if(self.is_winner(self.human)):
			print self.human+" wins the game"
			return 1

		self.whoseTurn()
		return 0

	
	def whoseTurn(self):
		countX = 0
		countO = 0
		for space in self.board:
			if(space == "O"):
				countO += 1
			elif(space == "X"):
				countX += 1
			
		print countO, countX
		if(countO == countX):
			if(self.turn != self.first):
				self.turn = self.first
				if(self.turn == self.robot):
					choice = self.get_computer_move()
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
				
		


	def robotMove(self, choice):
		#make robot move to coordinates based on choice
		print 'robot chose '+str(choice)
		choice -= 1
		if(self.y[choice] >= 0):
			arm = 'l'
		else:
			arm = 'r'

		move_arm(self.x[choice], self.y[choice], self.z[choice], 1.0, arm)



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
		
	def is_board_full(self, board = None):
		if board == None:
			board = self.board
		if " " in board:
			return False
		else:
			return True
			
			
	def humanMove(self):
		print 'human move'
		choice = 0
		while(self.board[choice] != " "):
			choice = raw_input("Please choose an empty space for "+self.human+" ")
			choice = int(choice)
			if self.board[choice] == " ":
				#call move arm to set the choice
				break
			else:
				print "Sorry, that space is not empty!"
				time.sleep(1)
		
		#automatically make piece appear in specified choice in gazebo
		
		
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
	'''
		##This AI is random
		##A better AI should take into account the board, the pieces etc.
		#This AI is good enough for the robotics project, and only if there's time 
		#  is it worth fleshing out the strongest AI

		#if the center square is empty choose that
		if self.board[5] == " ":
			return 5

		while True:
			move = random.randint(1,9)
			#if the move is blank, go ahead and return, otherwise try again
			if self.board[move] == " ":
				return move
				break
			
		return 5
'''

def callback(msg):
	global game
	
	if(game == None):
		game = TTTGame()

	#don't care about board until the game is started
	if(game.init == False):
		return

	result = game.updateBoard(msg.state, msg.x, msg.y, msg.z)
	if(result == 1):
		game = TTTGame()


if __name__ == '__main__':
	rospy.init_node('game')
	global game
	rospy.Subscriber("board_finder/TicTacToe", TicTacToe, callback)
	print("Starting game node")
	rospy.spin()

#Main function 	

#Who goes first?
'''
first = raw_input("Who goes first? (1 = Computer, 2 = Human)")
first = int(first)
if first == 1:
	choice = get_computer_move(board,  "O")
	board[choice] = "O"
	
while True:
	os.system("clear")
	print_header()
	print_board()


	
	#Check to see if the space is empty first
	tmp = 1
	while (tmp == 1):
		#Get Player X Input
		choice = raw_input("Please choose an empty space for X. ")
		choice = int(choice)
		if board[choice] == " ":
			board[choice] = "X"
			tmp = 0
		else:
			print "Sorry, that space is not empty!"
			time.sleep(1)


		
	#Check for X win
	if is_winner(board, "X"):
		os.system("clear")
		print_header()
		print_board()
		print "X wins! Congratulations"
		break
		
	os.system("clear")
	print_header()
	print_board()
	
	#Check for a tie (is the board full)
	#If the board is full, do something
	if is_board_full(board):
		print "Tie!"
		break
	
	#Get Player O Input
	choice = get_computer_move(board,  "O")
	
	#Check to see if the space is empty first
	if board[choice] == " ":
		board[choice] = "O"
	else:
		print "Sorry, that space is not empty!"
		time.sleep(1)
		
	#Check for O win
	if is_winner(board, "O"):
		os.system("clear")
		print_header()
		print_board()
		print "O wins! Congratulations"
		break
		
	#Check for a tie (is the board full)
	#If the board is full, do something
	if is_board_full(board):
		print "Tie!"
		break
	
'''

	
	
	
