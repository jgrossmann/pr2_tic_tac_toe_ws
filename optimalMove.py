#!/usr/bin/env python

def winGame(board, shape):
		
	if(board[0] == shape and board[4] == shape and board[8] == shape):
		return True;
		
	if(board[2] == shape and board[4] == shape and board[6] == shape):
		return True;

	for i in range(0, 3):
		if(board[i] == shape and board[i+3] == shape and board[i+6] == shape):
			return True;
	
	for i in range(0, 7, 3):
		if(board[i] == shape and board[i+1] == shape and board[i+2] == shape):
			return True;
			
	return False;
	
def tieGame(board):
	for space in board:
		if(space == ' '):
			return False
	return True
		

	
def getOptimalMove(board, shape, otherShape):
	
	index = 0
	bestMove = None
	for space in board:
		
		if(space == ' '):
			tempBoard = board[:]
			tempBoard[index] = shape
			if(winGame(tempBoard, shape)):
				return (index, -10)
			
			elif(tieGame(tempBoard)):
				return (index, 0)
				
			else:
				move = getOptimalMove(tempBoard, otherShape, shape)
				if(bestMove == None):
					bestMove = (index, move[1])
				else:
					if(move[1] > bestMove[1]):
						bestMove = (index, move[1])
				
		index += 1
	return (bestMove[0], -bestMove[1])
				
		
def printBoard(board):
	print ''
	for i in range(0,9):
		if(board[i] == ' '):
			print '_',
		else:
			print board[i],
		
		if((i+1)%3 == 0):
			print ""

if __name__ == '__main__':
	board = ['X', ' ', 'O',	' ', 'X', ' ', 'O', ' ', ' ']
	curShape = 'O'
	otherShape = 'X'
	move = getOptimalMove(board, curShape, otherShape)
	while(move != None):
		board[move[0]] = curShape

		printBoard(board)
		print move
		if(winGame(board, curShape)):
			print curShape+' has won the game'
			break
			
		elif(tieGame(board)):
			print 'tie game'
			break
		else:
			if(curShape == 'O'):
				curShape = 'X'
				otherShape = 'O'
			else:
				curShape = 'O'
				otherShape = 'X'
			move = getOptimalMove(board, curShape, otherShape)

				
				
