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
    def __init__(self):
        self.b = getFullBoard()
        
        self.player_1 = getPlayer('black','0')
        self.player_2 = getPlayer('white','0')

        piece = self.player_1.removePiece(self.b)
        self.b = rmPiece(piece, self.b)

        piece = self.player_2.removePiece(self.b, piece)
        self.b = rmPiece(piece, self.b)

        while(1):
            self.turn(self.player_1)
            self.turn(self.player_2)

    def turn(self, player):
        self.b = player.movePiece(self.b)

def getPlayer(color,p_type=None):
    print "Player Type for {0} pieces".format(color)
    print "0 - Real Player"

    if p_type == None:
        p_type = raw_input(' >>> ')

    if p_type == '0':
        return player.Player(color)

    print "Incorrect Option"
    return getPlayer(color)

if __name__ == '__main__':
    Game()
