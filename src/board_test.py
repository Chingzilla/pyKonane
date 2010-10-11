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

        self.board_array = [[1, 0, 1, 0, 1, 1],
                            [1, 1, 1, 1, 1, 1], 
                            [1, 1, 0, 1, 1, 1], 
                            [1, 1, 0, 1, 1, 1], 
                            [1, 1, 1, 1, 1, 1], 
                            [1, 1, 1, 1, 1, 1]]

        self.b_1 = b.arrayToBoard(self.board_array)
        
    def test_getMask(self):
        self.assertEqual(b.getMask(5), 2**5)
        self.assertEqual(b.getMask([0,1]), 3)

    def test_getN(self):
        self.assertEqual(b.getN(5,0), 5)
        self.assertEqual(b.getN(1,7), 1 + 7*6)

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

        

if __name__ == '__main__':
    unittest.main()
