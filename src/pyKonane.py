#!/usr/bin/env python
#src/pyKonane.py

import sys
from board import *
import player

COLOR = {'red':0, 'black':1}

class Game:
    '''
    Stores a game instance
    '''
    def __init__(self,size=None,player_1=None,player_2=None):
        #setboard size
        changeBoardSize(int(raw_input("Size of Board? ")))
        print SIZE

        self.b = getFullBoard()
        
        self.player_1 = getPlayer('black','1')
        self.player_2 = getPlayer('white','1')

        piece = self.player_1.removePiece(self.b)
        self.b = rmPiece(piece, self.b)

        piece = self.player_2.removePiece(self.b, piece)
        self.b = rmPiece(piece, self.b)

        rounds = 0

        while(1):
            rounds += 1
            
            self.turn(self.player_1)
            #Does White Have moves?
            if not getListOfMoves(self.b)[1]:
                print "--- Black Player Wins!!! ---"
                break

            self.turn(self.player_2)
            #Does Black Have moves?
            if not getListOfMoves(self.b)[0]:
                print "--- White Player Wins!!! ---"
                break

        #print toString(self.b)
        print "Game ended in {0} rounds.".format(rounds)
        print "Number of Boards looked at: {0}".format(len(known_boards))
        sys.exit(0)

    def turn(self, player):
        self.b = player.movePiece(self.b)

def getPlayer(color,p_type=None):
    print "Player Type for {0} pieces".format(color)
    print "0 - Real Player"
    print "1 - Randomn Player"

    if p_type == None:
        p_type = raw_input(' >>> ')

    if p_type == '0':
        return player.Player(color)
    if p_type == '1':
        return player.Player_Random(color)

    print "Incorrect Option"
    return getPlayer(color)

if __name__ == '__main__':
    Game()
