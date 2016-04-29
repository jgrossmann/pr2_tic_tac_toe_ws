#Import
import os
import time
import random

#Define the board
board = ["", " ", " ", " ", " ", " ", " ", " ", " ", " "]

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

class TTTGame:
	board = None 
	turn = None
	first = None
	robot = None
	human = None
	finishedTurn = False
	
	
	def __init__(self):
		board = ["", " ", " ", " ", " ", " ", " ", " ", " ", " "]
		#set the first to go and robot shape
		#don't pick move until we have a game board in vision
		#use vision callback to decide move
		first = raw_input("Who goes first? (1 = Computer, 2 = Human)")
		first = int(first)
		if first == 1:
			self.robot = "O"
			self.first = robot
			self.human = "X"
			self.turn = robot
		else:
			self.robot = "X"
			self.human = "O"
			self.first = human
			self.turn = human
			
	
	def updateBoard(self, visionBoard):
		
		index = 1
		for space in visionBoard:
			if(space == 0):
				board[index] = " "
			elif(space == 1):
				board[index] = "O"
			elif(space == 2):
				board[index] = "X"
			else:
				print ('bad value in board')
	
	def whoseTurn(self):
		countX = 0
		countO = 0
		for space in self.board:
			if(space == "O"):
				countO += 1
			elif(space == "X"):
				countX += 1
			
			
		if(countO == countX):
			if(self.turn != self.first):
				self.turn = self.first
				if(self.turn == self.robot):
					self.get_computer_move()
				else:
					
			self.turn = self.first
						
		if(countO > countX):
			if(self.robot == "O"):
				
					
		if(self.robot != self.turn):
			turnFinished = True

	#Define the print_board function 
	def print_board(self):
		print "   |   |   "
		print " "+board[1]+" | "+board[2]+" | "+board[3]+"  "
		print "   |   |   "
		print "---|---|---"
		print "   |   |   "
		print " "+board[4]+" | "+board[5]+" | "+board[6]+"  "
		print "   |   |   "
		print "---|---|---"
		print "   |   |   "			
		print " "+board[7]+" | "+board[8]+" | "+board[9]+"  "
		print "   |   |   "
	
	def is_winner(self, board, player):
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
		
	def is_board_full(board):
		if " " in board:
			return False
		else:
			return True
			
			
	def getHumanMove(self):
		
		while(board[choice] != " "):
			choice = raw_input("Please choose an empty space for "+self.human)
			choice = int(choice)
			if board[choice] == " ":
				#call move arm to set the choice
				break
			else:
				print "Sorry, that space is not empty!"
				time.sleep(1)
		
		return choice
		
		
	def get_computer_move(self):
	


		##This AI is random
		##A better AI should take into account the board, the pieces etc.
		#This AI is good enough for the robotics project, and only if there's time 
		#  is it worth fleshing out the strongest AI

		#if the center square is empty choose that
		if board[5] == " ":
			return 5

		while True:
			move = random.randint(1,9)
			#if the move is blank, go ahead and return, otherwise try again
			if board[move] == " ":
				return move
				break
			
		return 5


#Main function 	

#Who goes first?
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
	


	
	
	
