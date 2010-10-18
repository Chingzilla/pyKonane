#!/usr/bin/env python
#src/board_test.py

import unittest
import board
from board import getMask, getN

#create shorthands
global b, m, n
b = board
m = getMask
n = getN

class TestBoardFunctions(unittest.TestCase):
    def setUp(self):
        b.SIZE = 6

        board_array = [[1, 0, 1, 0, 1, 1],
                       [1, 1, 1, 1, 1, 1], 
                       [1, 1, 0, 1, 1, 1], 
                       [1, 1, 0, 1, 1, 1], 
                       [1, 1, 1, 1, 1, 1], 
                       [1, 1, 1, 1, 1, 1]]

        self.b_1 = b.arrayToBoard(board_array)

        self.m_1_1 = b.mvPiece(5,3,self.b_1)
        self.m_1_2 = b.mvPiece(5,1,self.b_1)
        self.m_1_3 = b.mvPiece(b.getN(1,2), b.getN(1,0), self.b_1)
        

    def test_getValidMoviesInDirect(self):
        self.assertEqual(b.getValidMoviesInDirect(self.b_1, 1, 1), [self.m_1_2])

    def test_getValidMovies(self):
        self.assertEqual(b.getValidMovies(self.b_1, 1), [b.mvPiece(5,1,self.b_1), b.mvPiece(13,1,self.b_1)])
        
        
    def test_getListOfMovies(self):

        board_array = [[1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1], 
                       [1, 1, 0, 1, 1, 1], 
                       [1, 1, 0, 1, 1, 1], 
                       [1, 1, 1, 1, 1, 1], 
                       [1, 1, 1, 1, 1, 1]]

        self.b_2 = b.arrayToBoard(board_array)

        m_2_1 = b.mvPiece(b.getN(2,0), b.getN(2,2), self.b_2)
        m_2_2 = b.mvPiece(b.getN(0,2), b.getN(2,2), self.b_2)
        m_2_3 = b.mvPiece(b.getN(4,2), b.getN(2,2), self.b_2)
        m_2_4 = b.mvPiece(b.getN(0,3), b.getN(2,3), self.b_2)
        m_2_5 = b.mvPiece(b.getN(2,5), b.getN(2,3), self.b_2)
        m_2_6 = b.mvPiece(b.getN(4,3), b.getN(2,3), self.b_2)

        moves_2_w = [m_2_4, m_2_5, m_2_6].sort()
        moves_2_b = [m_2_1, m_2_2, m_2_3].sort()

        moves_2 = b.getListOfMovies(self.b_2)
        moves_2 = [moves_2[0].sort(), moves_2[1].sort()]

        self.assertEqual(moves_2, [moves_2_b, moves_2_w])

    def test_mvPiece(self):
        self.b_1 = b.getMask([0,1,3])
        self.assertEqual(b.mvPiece(0,2,self.b_1),b.getMask([3,2]))
        
        new_board = b.mvPiece(0,4, self.b_1)
        #print b.toString(new_board)
        self.assertEqual(new_board,b.getMask(4))
    
    def test_getMask(self):
        self.assertEqual(b.getMask(5), 2**5)
        self.assertEqual(b.getMask([0,1]), 3)

    def test_getN(self):
        self.assertEqual(b.getN(5,0), 5)
        self.assertEqual(b.getN(1,7), 1 + 7*6)

    def test_getXY(self):
        self.assertEqual(b.getXY(13),[1,2])
        self.assertEqual(b.getXY(2),[2,0])
        self.assertEqual(b.getXY(35),[5,5])
        self.assertEqual(b.getXY(25),[1,4])
        self.assertEqual(b.getXY(6),[0,1])

    def test_isBlack(self):
        #test isBlack
        self.assertTrue(b.isBlack(n(0,0)))
        self.assertTrue(b.isBlack(n(3,1)))
        self.assertTrue(not b.isBlack(n(0,1)))
        self.assertTrue(not b.isBlack(n(1,0)))

    def test_isPieceAt(self):
        self.assertTrue(b.isPieceAt(4,self.b_1))
        self.assertTrue(b.isPieceAt(35,self.b_1))
        self.assertTrue(not b.isPieceAt(3,self.b_1))
        self.assertTrue(not b.isPieceAt(14,self.b_1))

    def test_getDist(self):
        self.assertEqual(b.getDist(0,0), 0)
        self.assertEqual(b.getDist(0,3), 3)
        self.assertEqual(b.getDist(3,0), 3)
        self.assertEqual(b.getDist(7,19), 2)
        self.assertEqual(b.getDist(35,0), 0)

    def test_getDirection(self):
        self.assertEqual(b.getDirection(0,35), 0)
        self.assertEqual(b.getDirection(0,getN(5,0)),1)
        self.assertEqual(b.getDirection(0,n(0,5)), b.SIZE)
        self.assertEqual(b.getDirection(0,0), 0)
        self.assertEqual(b.getDirection(5,0), -1)
        self.assertEqual(b.getDirection(6,0), -b.SIZE)
        self.assertEqual(b.getDirection(0,0), 0)

    def test_getMoveMasks(self):
        self.assertEqual(b.getMoveMasks(0,2), (m([0,1]), m([2])))
        self.assertEqual(b.getMoveMasks(0,4), (m([0,1,3]), m([2,4])))
        self.assertEqual(b.getMoveMasks(0,12), (m([0,6]), m([12])))
        self.assertEqual(b.getMoveMasks(12,0), (m([12,6]), m([0])))
        self.assertEqual(b.getMoveMasks(0,2), (m([0,1]), m([2])))

    def test_getListOfPieces(self):
        self.assertEqual(b.getListOfPieces(11), [0,1,3])
        self.assertEqual(b.getListOfPieces(16), [4])

    def test_getRelitiveN(self):
        self.assertEqual(b.getRelitiveN(6,1,0),7)
        self.assertEqual(b.getRelitiveN(6,0,1),12)
        self.assertEqual(b.getRelitiveN(35,-1,-5),4)
        #Test invalid input
        self.assertEqual(b.getRelitiveN(5,1,0),-1)
        self.assertEqual(b.getRelitiveN(32,0,1),-1)
        
    
    ## Test check methods ##
    def test_checkOutOfBounds(self):
        self.assertTrue(b.checkOutOfBounds(5))
        self.assertTrue(b.checkOutOfBounds(b.SIZE**2 -1))
        self.assertTrue(not b.checkOutOfBounds(-1))
        self.assertTrue(not b.checkOutOfBounds(b.SIZE**2))
        self.assertTrue(not b.checkOutOfBounds(b.SIZE**2 + 4))

    def test_checkIfJump(self):
        self.assertTrue(b.checkIfJump(0,2))
        self.assertTrue(b.checkIfJump(2,0))
        self.assertTrue(b.checkIfJump(2,14))
        self.assertTrue(b.checkIfJump(35,31))
        self.assertTrue(not b.checkIfJump(0,0))
        self.assertTrue(not b.checkIfJump(1,0))
        self.assertTrue(not b.checkIfJump(5,0))
        self.assertTrue(not b.checkIfJump(0,7))
        self.assertTrue(not b.checkIfJump(0,6))
        self.assertTrue(not b.checkIfJump(6,11))

    def test_PlacesMaskchecks(self):
        self.assertTrue(b.checkIfPlacesTaken(1,7))
        self.assertTrue(b.checkIfPlacesTaken(2,7))
        self.assertTrue(b.checkIfPlacesTaken(3,7))
        self.assertTrue(not b.checkIfPlacesTaken(1,0))
        self.assertTrue(not b.checkIfPlacesTaken(7,3))

        self.assertTrue(b.checkIfPlacesAvalable(4,3))
        self.assertTrue(b.checkIfPlacesAvalable(5,2))
        self.assertTrue(not b.checkIfPlacesAvalable(3,2))
        self.assertTrue(not b.checkIfPlacesAvalable(7,7))

    ## Verify tests ##
    def test_isValidMove(self):
        self.assertTrue(b.isValidMove(5,3,self.b_1))
        self.assertTrue(b.isValidMove(5,1,self.b_1))
        self.assertTrue(not b.isValidMove(5,0,self.b_1))
        self.assertTrue(not b.isValidMove(3,5,self.b_1))
        self.assertTrue(not b.isValidMove(0,2,self.b_1))

    def test_isValidRemoveBlack(self):
        self.assertTrue(b.isValidRemoveBlack(0))
        self.assertTrue(b.isValidRemoveBlack(21))
        self.assertTrue(b.isValidRemoveBlack(14))
        self.assertTrue(b.isValidRemoveBlack(35))

        self.assertTrue(not b.isValidRemoveBlack(2))
        self.assertTrue(not b.isValidRemoveBlack(32))

    def test_isValidRemoveWhite(self):
        self.assertTrue(b.isValidRemoveWhite(1,0))
        self.assertTrue(b.isValidRemoveWhite(6,0))

        self.assertTrue(b.isValidRemoveWhite(15,14))
        self.assertTrue(b.isValidRemoveWhite(13,14))
        self.assertTrue(b.isValidRemoveWhite(8,14))
        self.assertTrue(b.isValidRemoveWhite(20,14))

        self.assertTrue(b.isValidRemoveWhite(22,21))
        self.assertTrue(b.isValidRemoveWhite(20,21))
        self.assertTrue(b.isValidRemoveWhite(15,21))
        self.assertTrue(b.isValidRemoveWhite(27,21))

        self.assertTrue(b.isValidRemoveWhite(34,35))
        self.assertTrue(b.isValidRemoveWhite(29,35))

        self.assertTrue(not b.isValidRemoveWhite(1,35))
        self.assertTrue(not b.isValidRemoveWhite(3,9))

if __name__ == '__main__':
    unittest.main()
