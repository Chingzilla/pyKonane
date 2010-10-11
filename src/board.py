#src/board.py

SIZE = 6

### Board pieces methods ###
def getMask(points):
    '''returns mask created from the n values'''
    if type(points) == int:
        return int(2**points)

    mask = 0
    for x in points:
        mask |= 2**x
    return int(mask)

def getN(col, row):
    return col + row * SIZE

def isBlack(n):
    return not ( n + (n / SIZE) % 2 ) % 2

def getDist(old_n, new_n):
    diff = abs(new_n - old_n)
    if diff < SIZE:
        return diff

    if not diff % SIZE:
        return diff / SIZE
    
    return 0

def getDirection(old_n, new_n):
    '''Returns the direction as an Int,
    {1,-1} if left/right
    {SIZE, -SIZE} if up/down
    {0} if on diginal or same place'''
    if old_n == new_n:
        return 0
    diff = new_n - old_n
    sign = diff / abs(diff)
    if abs(diff) < SIZE:
        return sign
    
    if not diff % SIZE:
        return sign * SIZE

    return 0

def isPieceAt(n, board):
    mask = getMask(n)
    return bool((mask & board) == mask) 

def getMoveMasks(old_n,new_n):
    rm_m = [old_n]
    mv_m = [new_n]

    dist = getDist(old_n,new_n)
    direct = getDirection(old_n,new_n)

    if dist==direct==0:
        return 0,0

    for i in range(1, dist):
        point = old_n + i * direct
        
        #If odd hop, remove peice
        if not i % 2:
            mv_m.append(point)
        else:
            rm_m.append(point)
    return getMask(rm_m), getMask(mv_m)

def getXY(n):
    return [n/SIZE, n%SIZE]

## Checks ##
# all checks return true if passed

def checkOutOfBounds(n):
    return bool(0 <= n < SIZE**2)

def checkIfJump(old_n, new_n):
    '''Checks if the jump is an even number, and that it is a move'''
    dist = getDist(old_n, new_n)
    if dist % 2 == 0 and dist !=0:
        return 1
    return 0

def checkIfPlacesTaken(mask, board):
    board = mask & board
    return mask == board

def checkIfPlacesAvalable(mask, board):
    board = mask & board
    return not bool(board)

## Verify methods ##
# all verify methods return true if passed

def isValidMove(old_n, new_n, board):
    
    # Proper Jump? (also checks if same color and that not same place)
    if not checkIfJump(old_n, new_n):
        return 0

    # In bounds?
    if not (checkOutOfBounds(old_n) or checkOutOfBounds(new_n)):
        return 0

    rm_m, mv_m = getMoveMasks(old_n, new_n)
    # All jump places avaliable?
    if not checkIfPlacesAvalable(mv_m, board):
        return 0

    # Are black peices being jumped?
    if not checkIfPlacesTaken(rm_m, board):
        return 0

    # All checks passed
    return 1




#i### Player based methods ###
#idef removePeice(x, y, board):
#i    n = getN(x,y)
#i    
#i    if not isPieceAtN(n,board):
#i        return 0
#i    else:
#i        return board - 2**n
#i
#i### Movement related Methods ###
#i
#idef movePiece(old_peice, new_peice, board):
#i    op = getN(old_place[0], old_place[1])
#i    np = getN(new_place[0], new_place[1])
#i
#i    return movePieceN(op, np, board)
#i
#idef movePieceN(op, np, board):
#i    if not isValidMoveN(op, np, board):
#i        return 0
#i
#i    while(op != np):
#i        if isBlackN(np) != isBlackN(op):
#i            board ^= op
#i        op = nextPeiceN(op)
#i    
#i    board ^= op
#i
#i    return 1 
#i
#idef getDistance(old_place, new_place):
#i    return abs(new_place[0] - old_place[0] + new_place[1] - old_place[1])
#i
#idef getDistanceN(old, new):
#i    return getDistance(getXY(old),getXY(new))
#i
#idef getDirection(old_place, new_place):
#i    direct_x = new_place[0] - old_place[0]
#i    direct_y = new_place[1] - old_place[1]
#i    
#i    if direct_x:
#i        direct_x = int(direct_x/abs(direct_x))
#i    if direct_y:
#i        direct_y = int(direct_y/abs(direct_y))
#i
#i    return [direct_x, direct_y]
#i
#idef getDirectionN(old, new):
#i    return getDirection(getXY(old), getXY(new))
#i
#idef getNumOfJumps(old_place, new_place):
#i    distance = getDistance(old_place, new_place)
#i    if distance % 2:
#i        return 0
#i    return abs(distance / 2)


### General Board methods ###
def getFullBoard():
    return (2**(6**2) -1)

def toArray(board):
    board_array = []
    for y in range(SIZE):
        board_array.append([])
        for x in range(SIZE):
            if(isPieceAt(getN(x,y),board)):
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
                board += 2**getN(x,y)
    
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
                if isBlack(getN(x,y)):
                    string += 'b'
                else:
                    string += 'w'
            else:
                string += ' '
    return string
