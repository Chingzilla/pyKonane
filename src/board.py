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
    n = int(getTileNum(x,y))
    return (int(2**n) & int(board))

def isPieceAtN(n,board):
    return (2**n & int(board))

def whatRow(n):
    return (n) / SIZE

def whatCol(n):
    return (n) % SIZE

def nextPiece(x,y,direction):
    '''
    returns the tile location in the given direction
    assumes: -that x,y are correct locations
             - direction is a unit vector
    '''
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

def getMoveMask(move):
    mask = move
    

def isValidMove(old_place, new_place, board):
    op = getTileNum(old_place[0], old_place[1])
    np = getTileNum(new_place[0], new_place[1])

    return isValidMoveN(op, np, board)

def isValidMoveN(op, np, board):

    # Get (x,y) for checks
    opxy = getXY(op)
    npxy = getXY(np)

    # check if out of bounds
    if not(0 <= op < SIZE**2 and 0 <= np < SIZE**2):
        return 0
    
    # check if same place
    if op == np: return 0

    # check if same color
    if isBlackN(op) != isBlackN(np): return 0

    # check if new place is taken
    if isPieceAtN(np, board): return 0

    # check if there is a peice at op
    if not isPieceAtN(op, board): return 0

    # Get the movement direction (scaled)
    direct_x, direct_y = getDirection(opxy,npxy)

    # check if move is horizontal xor vertial (no diaginal)
    if not (direct_x ^ direct_y): return 0

    # check if jumping over a opponent's piece
    if not isPieceAt(opxy[0] + direct_x, opxy[1] + direct_y, board):
        return 0

    # recursive call if more then one jump
    if getNumOfJumps(opxy, npxy) > 1:
        op = getTileNum(opxy[0] + 2 * direct_x, opxy[1] + 2 * direct_y)
        return isValidMoveN(op, np, board)

    return 1

### Movement related Methods ###

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

def getDistance(old_place, new_place):
    return abs(new_place[0] - old_place[0] + new_place[1] - old_place[1])

def getDirection(old_place, new_place):
    direct_x = new_place[0] - old_place[0]
    direct_y = new_place[1] - old_place[1]
    
    if direct_x:
        direct_x = int(direct_x/abs(direct_x))
    if direct_y:
        direct_y = int(direct_y/abs(direct_y))

    return [direct_x, direct_y]

def getNumOfJumps(old_place, new_place):
    distance = getDistance(old_place, new_place)
    if distance % 2:
        return 0
    return abs(distance / 2)


### General Board methods ###
def getFullBoard():
    return (2**(6**2) -1)

def toArray(board):
    board_array = []
    for y in range(SIZE):
        board_array.append([])
        for x in range(SIZE):
            if(isPieceAt(x,y,board)):
                board_array[y].append(1)
            else:
                board_array[y].append(0)
    return board_array

def arrayToBoard(board_array):
    '''Takes array in form array[y][x]'''
    #check if board is the right size
    if not len(board_array)==len(board_array[0])==SIZE:
        return 0

    board = 0
    for y in range(len(board_array)):
        for x in range(len(board_array[y])):
            if board_array[y][x]:
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
