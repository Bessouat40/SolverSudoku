board = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]


def ac3(pos, val, possibilite):
    possibilite=modifPossiLigne(pos[0], val, 0, possibilite)
    possibilite= modifPossiCol(pos[1], val, 0, possibilite)
    possibilite = modifPossiCarre(pos, val, 0, possibilite)
    return possibilite


def invAC3(pos, val, possibilite):
    possibilite=modifPossiLigne(pos[0], val, 1,possibilite)
    possibilite=modifPossiCol(pos[1], val, 1,possibilite)
    possibilite=modifPossiCarre(pos, val, 1,possibilite)
    return possibilite

def createPossibilities(board) :
    possibilite = [[[1 for i in range(1, 10)] for i in range(9)] for i in range(9)]
    for i in range (len(board)) :
        for j in range (len(board)):
            if board[i][j]!=0 :
                possibilite[i][j]=[0 for i in range(9)]
                possibilite = modifPossiLigne(i,board[i][j],0,possibilite)
                possibilite = modifPossiCol(j,board[i][j],0, possibilite)
                possibilite = modifPossiCarre([i,j],board[i][j], 0, possibilite)
    return possibilite

def modifPossiLigne(ligne, val, remp, possibilite):
    # On modofie les posisbilité de la ligne en fonction de la valeur posée
    possi = possibilite[ligne]
    for i in range(len(possi)):
        x = possi[i]
        x[val - 1] = remp  # val-1 car on commence à 0
        possi[i] = x
    possibilite[ligne] = possi
    return possibilite

def modifPossiCol( col, val, remp, possibilite):
    for i in range(len(possibilite)):
        possibilite[i][col][val-1]=remp
    return possibilite

def modifPossiCarre( pos, val, remp, possibilite):
    num_carre = retrouveCarre(pos[0], pos[1])
    carre = getCarre(num_carre, possibilite)
    indice = getIndicesCarre(num_carre)
    for i in range (len(carre)) :
        carre[i][val-1]=remp
    for j in range (len(carre)) :
        possibilite[indice[j][1]][indice[j][0]]=carre[j]
    return possibilite

def getIndicesCarre(n):
    n2 = n - 1
    x = (n2 % 3) * 3
    y = (n2 // 3) * 3
    indices = [[y + i, x + j] for i in range(3) for j in range(3)]
    return indices

def getCarre( i, possibilite):
    indices = getIndicesCarre(i)
    sudoku = possibilite
    carre = []
    for l in indices:
        carre.append(sudoku[l[1]][l[0]])
    return carre

def retrouveCarre( x, y):
    carre = (y // 3) * 3 + 1 + x // 3
    return carre

def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1,10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            if solve(bo):
                return True

            bo[row][col] = 0

    return False


def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False

    return True


def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col

    return None

print_board(board)
solve(board)
print("___________________")
print_board(board)