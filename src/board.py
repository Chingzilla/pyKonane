#src/board.py

SIZE = 6

### Board pieces methods ###
def isBlack(col,row):
    return (col + row + 1) % 2

def isBlackN(n):
    return (sum(getXY(n)) + 1) % 2

def getXY(n):
    return [whatCol(n), whatRow(n)]
    
def getTileNum(col,row):
    return col + row * SIZE

def isPieceAt(x,y,board):
    n = getTileNum(x,y)
    return (2**n & board)

def isPieceAtN(n,board):
    return (2**n & board)

def whatRow(n):
    return (n) / SIZE

def whatCol(n):
    return (n) % SIZE

def nextPiece(x,y,direction):
    '''
    returns the tile location in the given direction
    assumes: -that x,y are correct locations
             - direction is a unit vector'''
    return [x + direction[0], y + direction[1]]

def nextPieceN(n, direction):
    return n + direction[0] + direction[1]*SIZE

### Player based methods ###
def removePeice(x, y, board):
    n = getTileNum(x,y)
    
    if not isPieceAtN(n,board):
        return 0
    else:
        return board - 2**n

def isValidMove(old_place, new_place, board):
    op = getTileNum(old_place[0], old_place[1])
    np = getTileNum(new_place[0], new_place[1])

    return isValidMoveN(op, np, board)

def isValidMoveN(op, np, board):

    # Get (x,y) for checks
    opx, opy = getXY(op)
    npx, npy = getXY(np)

    # check if out of bounds
    if not(0 <= op < SIZE**2 and 0 <= np < SIZE**2):
        return 0
    
    # check if same place
    if op == np: return 0

    # check if same color
    if isBlackN(op) != isBlack(np): return 0

    # check if new place is taken
    if isPieceAtN(np): return 0

    # check if there is a peice at op
    if not isPieceAtN(op): return 0

    # Get the movement direction (scaled)
    direction = [opx - npx, opy -npy]
    direction = [direction[0]/abs(direction[0]),
                 direction[1]/abs(direction[1])]

    # check if move is horizontal xor vertial (no diaginal)
    if direction[0] ^ direction[1]: return 0

    # check if jumping over a opponent's piece
    if not isPieceAt(opx + direction[0], opy + direction[1]):
        return 0

    # recursive call if more then one jump
    if abs(direction[0] + direction[1]) > 1:
        op = getTileNum(opx + direction[0], opy + direction[1])
        return isValidMoveN(op, np, board)

    return 1
    
def movePiece(old_peice, new_peice, board):
    op = getTileNum(old_place[0], old_place[1])
    np = getTileNum(new_place[0], new_place[1])

    return movePieceN(op, np, board)

def movePieceN(op, np, board):
    if not isValidMoveN(op, np, board):
        return 0

    while(op != np):
        if isBlackN(np) != isBlackN(op):
            board ^= op
        op = nextPeiceN(op)
    
    board ^= op

    return 1 

### General Board methods ###
def getFullBoard():
    return (2**(6**2) -1)

def toArray(board):
    board_array = []
    for y in range(SIZE):
        board_array.append([])
        for x in range(SIZE):
            board_array[y].append(isPieceAt(x,y,board))
    return board_array

def arrayToBoard(board_array):
    
    #check if board is the right size
    if not len(board_array)==len(board_array[0])==SIZE:
        return 0

    board = 0
    for x in range(len(board_array)):
        for y in range(len(board_array[x])):
            if board_array[x][y]:
                board += 2**getTileNum(x,y)
    
    return board

def toString(board):
    '''Serialize board to string'''
    
    board = toArray(board)
    string = '    '
    for i in range(len(board[0])): string += '{0:3d}'.format(i)

    string += '\n    '

    for i in range(len(board)): string += '---'

    for x in range(len(board)):
        string += '\n{0:3d}|'.format(x)
        for y in range(len(board)):
            string += '  '
            if board[x][y]:
                if isBlack(x,y):
                    string += 'b'
                else:
                    string += 'w'
            else:
                string += ' '
    return string
