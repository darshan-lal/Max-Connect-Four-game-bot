from MaxConnect4Game import *
import copy

class alfaminmax:
	def __init__(self, currentGame, depth):
		
		#transfering the values to local variables
		self.currentTurn = currentGame.currentTurn
		#getting whose turn it is
		
		self.game = currentGame
		#gameboard

		self.treedepth = int(depth)
		#tree depth

	#max play	
	def maxplay(self, state, a, b):
		if state.pieceCount == 42 or state.nodeDepth == self.treedepth:
			return self.utility(state)
		val = -99999

		for y in availableMoves(state.gameBoard):
			newState = playmove(state,y)

			val = max(val,self.minplay( newState,a,b ))
			if val >= b:
				return val
			a = max(a, val)
		return val

	#min play
	def minplay(self, state, a, b):
		if state.pieceCount == 42 or state.nodeDepth == self.treedepth:
			return self.utility(state)
		val = 99999

		for x in availableMoves(state.gameBoard):
			newState = playmove(state,x)

			val = min(val,self.maxplay( newState,a,b ))
			if val <= a:
				return val
			b = min(b, val)
		return val

	#Utility for alpha beta pruning
	def utility(self,state):
		if self.currentTurn == 1:
			utility = state.player1Score * 2 - state.player2Score
		elif self.currentTurn == 2:
			utility = state.player2Score * 2 - state.player1Score

		return utility
	
	#chose the best move
	def chosemove(self):

			availmoves = availableMoves(self.game.gameBoard)
			minval=[]
			for z in availmoves:
				plmove = playmove(self.game,z)
				minval.append( self.minplay(plmove,99999,-99999) )
			chosen = availmoves[minval.index( max( minval ) )]
			return chosen

		

#play the move	
def playmove(current, column):
	#new board
	try:
		new = maxConnect4Game()
	except:
		print "error can't access gameboard"

	try:
		new.nodeDepth = current.nodeDepth + 1
	except:
		new.nodeDepth = 1

	#copying al the moves to new board including the current move
	try:
		new.pieceCount = current.pieceCount
		new.gameBoard = copy.deepcopy(current.gameBoard)
	except:
		print "can't copy the boards system error"

	if not new.gameBoard[0][column]:
		for i in range(5, -1, -1):
			if not new.gameBoard[i][column]:
				new.gameBoard[i][column] = current.currentTurn
				new.pieceCount += 1
				break
	
	#changing turns
	if current.currentTurn == 1:
		new.currentTurn = 2
	elif current.currentTurn == 2:
		new.currentTurn = 1
	new.checkPieceCount()
	new.countScore()

	return new

	#check for availabe moves
def availableMoves(gameboard):
	#available moves list
	availableMoves = []

	for columns, value in enumerate(gameboard[0]):
		try:
			if value == 0:
				availableMoves.append(columns)
		except:
			print "no available moves"
	return availableMoves

