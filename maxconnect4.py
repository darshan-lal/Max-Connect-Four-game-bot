#!/usr/bin/env python

# Written by Chris Conly based on C++
# code provided by Dr. Vassilis Athitsos
# Written to be Python 2.4 compatible for omega

import sys
from MaxConnect4Game import *
from alfaminmax import *

def oneMoveGame(currentGame,depth):
    if currentGame.pieceCount == 42:    # Is the board full already?
        print 'BOARD FULL\n\nGame Over!\n'
        sys.exit(0)

    #currentGame.aiPlay() # Make a move (only random is implemented)
    minmaxtree = alfaminmax(currentGame,depth)
    aimove = minmaxtree.chosemove()
    play = currentGame.playPiece(aimove)

    #display the current score
    print("\n\nMove no. %d: Player %d, column %d\n" % (currentGame.pieceCount, currentGame.currentTurn, aimove+1))
            
    #changing the turn
    if currentGame.currentTurn == 1:
        currentGame.currentTurn = 2
    elif currentGame.currentTurn == 2:
        currentGame.currentTurn = 1

    #displaying the game board
    print "Game board :"
    currentGame.printGameBoard()

    currentGame.countScore()
    print("Score: Player 1 = %d, Player 2 = %d\n" % (currentGame.player1Score, currentGame.player2Score))

    currentGame.gameFile.close()

def interactiveGame(currentGame,depth):

    while currentGame.pieceCount != 42:
        #if borad is not full enter


        if currentGame.currentTurn == 1:
            #if player its player 1 turn enter
            
            yourturn = input("Your turn! Enter the column no. (1-7): ")
            #Getting the input of the user from command line
            
            if not 0 < yourturn < 8:

                #check if its a valid move or not
                print "Invalid move!"
                continue

            if not currentGame.playPiece(yourturn-1):

                #if entered column is full  
                print "The column no. you entered is full please select other column!"
                continue

            try:

                #trying to open the usermove file
                currentGame.gameFile = open("usermove.txt", "w")
            except:

                #unable to open the file then shoot an error
                sys.exit('Error opening output file.')

            #display the current score
            print("\n\nMove no. %d: Player %d, column %d\n" % (currentGame.pieceCount, currentGame.currentTurn, yourturn))
            
            #changing the turn
            if currentGame.currentTurn == 1:
                currentGame.currentTurn = 2
            elif currentGame.currentTurn == 2:
                currentGame.currentTurn = 1

            #displaying the game board
            print "Game board :"
            currentGame.printGameBoard()

            currentGame.countScore()
            print("Score: Player 1 = %d, Player 2 = %d\n" % (currentGame.player1Score, currentGame.player2Score))

            currentGame.printGameBoardToFile()



        elif currentGame.pieceCount != 42:

            #If board is not full
            minmaxtree = alfaminmax(currentGame,depth)
            iaimove = minmaxtree.chosemove()
            play = currentGame.playPiece(iaimove)

            try:
                #trying to open the aimove file
                currentGame.gameFile = open("aimove.txt", 'w')
            except:
                #unable to open the file then shoot an error
                sys.exit("Unable to open output file.")

            print('\n\nMove no. %d: Player %d, column %d\n' % (currentGame.pieceCount, currentGame.currentTurn, iaimove+1))
            
            #changing the turns
            if currentGame.currentTurn == 1:
                currentGame.currentTurn = 2
            elif currentGame.currentTurn == 2:
                currentGame.currentTurn = 1

            #displaying the game board
            print "Game board :"
            currentGame.printGameBoard()

            currentGame.countScore()
            print("Score: Player 1 = %d, Player 2 = %d\n" % (currentGame.player1Score, currentGame.player2Score))

            currentGame.printGameBoardToFile()

    #closing the game file
    currentGame.gameFile.close()

    #Displaying the winner of the game
    if currentGame.player1Score > currentGame.player2Score:
        print "Congratulations you (Player 1) won the connect 4 game"
    elif currentGame.player2Score > currentGame.player1Score:
        print "Yeah! I win (Computer wins)"
    else:
        print "Well played it's a draw"



def main(argv):
    # Make sure we have enough command-line arguments
    if len(argv) != 5:
        print 'Four command-line arguments are needed:'
        print('Usage: %s interactive [input_file] [computer-next/human-next] [depth]' % argv[0])
        print('or: %s one-move [input_file] [output_file] [depth]' % argv[0])
        sys.exit(2)

    game_mode, inFile = argv[1:3]

    if not game_mode == 'interactive' and not game_mode == 'one-move':
        print('%s is an unrecognized game mode' % game_mode)
        sys.exit(2)

    currentGame = maxConnect4Game() # Create a game

    # Try to open the input file
    try:
        currentGame.gameFile = open(inFile, 'r')
    except IOError:
        sys.exit("\nError opening input file.\nCheck file name.\n")

    # Read the initial game state from the file and save in a 2D list
    file_lines = currentGame.gameFile.readlines()
    currentGame.gameBoard = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]
    currentGame.currentTurn = int(file_lines[-1][0])
    currentGame.gameFile.close()

    print '\nMaxConnect-4 game\n'
    print 'Game state before move:'
    currentGame.printGameBoard()

    # Update a few game variables based on initial state and print the score
    currentGame.checkPieceCount()
    currentGame.countScore()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))

    if game_mode == 'interactive':
        if argv[3] == 'computer-next': #override current turn according to commandline arguments
            currentGame.currentTurn = 2
        else: #human-next
            currentGame.currentTurn = 1
        interactiveGame(currentGame,argv[4]) # Be sure to pass whatever else you need from the command line
    else: # game_mode == 'one-move'
        # Set up the output file
        outFile = argv[3]
        try:
            currentGame.gameFile = open(outFile, 'w')
        except:
            sys.exit('Error opening output file.')
        oneMoveGame(currentGame,argv[4]) # Be sure to pass any other arguments from the command line you might need.


if __name__ == '__main__':
    main(sys.argv)



