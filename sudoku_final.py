import numpy as np
import sys

from numpy.core.numeric import indices

class Solver:
    def __init__(self, sudoku=[[0 for i in range(9)] for i in range(9)]):
        self.sudoku = sudoku
        self.possibilite = [[[1 for i in range(1, 10)] for i in range(9)] for i in range(9)]
        self.count = 0
        self.fixe = [[] for i in range(9)]

    def ajouterSudoku(self):
        print("Veillez entrer le sudoku ligne par ligne en séparant les chiffres par des virgules")
        print("(Remplacer les cases vide par la valeur 0 SVP)")
        grid = []
        while len(grid) < 9:
            try:
                arr = [int(x) for x in input().split(',')]
            except:
                print("Entrez uniquement des entiers séparés de virgules SVP")
            if len(arr) == 9:
                grid.append(arr)
            else:
                print("Entrer une ligne conforme SVP")
        return grid

    def InitPossi(self) :
        for i in range(len(self.sudoku)) :
            for j in range(len(self.sudoku[0])) :
                self.fixe[i].append(self.sudoku[i][j])
                if self.sudoku[i][j] != 0 :
                    self.possibilite[i][j] = [0 for i in range(9)]
                    val = self.sudoku[i][j]
                    pos = [i,j]
                    self.AC3(pos, val)

    def getSudoku(self):
        return self.sudoku

    def getPossibilites(self):
        return self.possibilite

    def getCarre(self, i):
        indices = self.getIndicesCarre(i)
        sudoku = self.getPossibilites()
        carre = []
        for l in indices:
            carre.append(sudoku[l[1]][l[0]])
        return carre

    def getIndicesCarre(self, n):
        n2 = n - 1
        y = (n2 % 3) * 3
        x = (n2 // 3) * 3
        indices = [[x + i, y + j] for i in range(3) for j in range(3)]
        return indices

    def zero_sudo(self) :
        pos = []
        for i in range(len(self.sudoku)) :
            for j in range(len(self.sudoku[0])) :
                if self.sudoku[i][j] == 0 :
                    pos.append([i,j])
        return pos

    def printSudoku(self):
        for k, i in enumerate(self.getSudoku()):
            if k%3 == 0 :
                print(' ---------------------')
            res = ''
            for num, j in enumerate(i):
                if num%3==0 :
                    res+='|'
                res+=str(j)
                res+=' '
            print(res+'|')

    def printPossibilites(self):
        for i in self.getPossibilites():
            print(i)
        print('\n')


    def ajoutSudoku(self, sudoku):
        if len(sudoku) != 9 or len(sudoku[0]) != 9:
            print("La taille du sodoku n'est pas conforme. Veuillez rentrer une grille de taille 9x9.")
        else:
            self.sudoku = sudoku

    def modifPossiLigne(self, ligne, val, remp):
        # On modofie les posisbilité de la ligne en fonction de la valeur posée
        possi = self.possibilite[ligne]
        for i in range(len(possi)):
            x = possi[i]
            x[val - 1] = remp  # val-1 car on commence à 0
            possi[i] = x
        self.possibilite[ligne] = possi

    def modifPossiCol(self, col, val, remp):
        for i in range(len(self.possibilite)):
            self.possibilite[i][col][val-1]=remp

    def retrouveCarre(self, x, y):
        ligne = [[1,2,3], [4,5,6], [7,8,9]]
        colonne = [[1,4,7], [2,5,8], [3,6,9]]
        comm = list(set(ligne[x//3]).intersection(colonne[y//3]))[0]
        return comm

    def posCarre(self, nb_carre):
        x = ((nb_carre - 1) % 3) * 3
        y = (((nb_carre - 1) // 3)) * 3
        return x, y

    def modifPossiCarre(self, pos, val, remp):
        num_carre = self.retrouveCarre(pos[0], pos[1])
        carre = self.getCarre(num_carre)
        indice = self.getIndicesCarre(num_carre)
        for i in range (len(carre)) :
            carre[i][val-1]=remp
        for j in range (len(carre)) :
            self.possibilite[indice[j][1]][indice[j][0]]=carre[j]

    def mrv(self, zeros) :
        pos = []
        mini = 1000
        for i in zeros :
            res = []
            res.append(self.sudoku[i[0]])
            res.append(list(np.array(self.sudoku)[:,i[1]]))
            carre = self.retrouveCarre(i[0], i[1])
            indice = self.getIndicesCarre(carre)
            for j in indice :
                res.append([self.sudoku[j[0]][j[1]]])
            res = sum(res, [])
            res = list(set(res))
            nbr = 9 - len(res)
            if 0 in res :
                nbr += 1
            if nbr < mini and nbr > 0 :
                mini = nbr
                pos = [i]
            elif nbr == mini and nbr > 0 :
                pos.append(i)
            
        return pos

    def AC3(self, pos, val) :
        self.modifPossiLigne(pos[0], val, 0)
        self.modifPossiCol(pos[1], val, 0)
        self.modifPossiCarre(pos, val, 0)

    def degreeHeuristic(self, zeros) :
        pos = []
        maxi = -10
        indices = []
        for i in zeros :
            i_l = [[i[0],j] for j in range(9)]
            i_c = [[j, i[1]] for j in range(9)]
            for j in range(9) :
                if  not(i_l[j] in indices) :
                    indices.append(i_l[j])
                if  not(i_c[j] in indices) :
                    indices.append(i_c[j])
            carre = self.retrouveCarre(i[0], i[1])
            indice = self.getIndicesCarre(carre)
            for j in indice :
                if not(j in indices) :
                    indices.append(j)
            res = 0
            for j in indices :
                if self.sudoku[j[0]][j[1]] == 0 :
                    res += 1
            if res > maxi and res > 0 :
                maxi = res
                pos = [i]
            elif res == maxi and res > 0 :
                pos.append(i)
            
        return pos

    def possible_col(self, pos, val) :
        col = np.asarray(self.sudoku)[:,pos[1]]
        return not(val in col)
    
    def possible_ligne(self, pos, val) :
        ligne = np.asarray(self.sudoku)[pos[0]]
        return not(val in ligne)

    def possible_carre(self, pos, val) :
        num_carre = self.retrouveCarre(pos[0], pos[1])
        indice = self.getIndicesCarre(num_carre)
        res = []
        for i in indice :
            res.append(self.sudoku[i[0]][i[1]])
        return not(val in res)

    def possible(self, pos, val) :
        return self.possible_col(pos, val) and self.possible_carre(pos, val) and self.possible_ligne(pos, val)


    def solve(self) :
        find = self.zero_sudo()
        if len(find) == 0 :
            return True
        else:
            l = self.mrv(find)[0] # rajout
            #row, col = find[0]
            row, col = l[0]
        for i in range(1,10):
            if self.possibilite[row][col][i-1]==1:
                print('i : ',i)
                print('possibilite : ', self.possibilite)
                print('pos : ',[row,col])
                self.printSudoku()
                self.sudoku[row][col] = i
                self.AC3([row,col],i)
                if self.solve() :
                    return True
                self.InvAC3([row,col],i)
                self.sudoku[row][col] = 0
        return False

    def solve2(self) :
        find = self.zero_sudo()
        print('find : ', find)
        if len(find) == 0 :
            print('finito pipo')
            return True
        else : 
            l = self.mrv(find) 
            print('l mrv : ',l)
            if len(l) != 0 :
                l = self.degreeHeuristic(l)
                print('l DH : ',l)
            row, col = l[0]
        for i in range(1,10):
            if self.possible([row,col],i) :
                self.sudoku[row][col] = i
                if self.solve2() :
                    return True
                #self.AC3([row,col], i)
            self.sudoku[row][col] = 0
        return False

if __name__ == "__main__":
    solver = Solver()
    grille = [[7, 3, 4, 0, 0, 0, 0, 0, 1],
              [0, 5, 0, 0, 9, 8, 0, 0, 3],
              [0, 9, 0, 0, 1, 4, 0, 5, 2],
              [3, 0, 2, 4, 0, 6, 8, 0, 0],
              [0, 0, 9, 1, 0, 3, 2, 0, 0],
              [0, 0, 5, 9, 0, 2, 6, 0, 4],
              [9, 2, 0, 5, 6, 0, 0, 4, 0],
              [1, 0, 0, 2, 4, 0, 0, 9, 0],
              [5, 0, 0, 0, 0, 0, 1, 2, 7]]
    
    grille2 = [[0,3,0,0,5,7,1,0,0],
               [0,5,0,0,2,0,0,0,0],
               [0,0,0,0,0,0,0,7,0],
               [0,0,0,6,8,0,0,0,3],
               [0,6,3,0,0,0,0,0,1],
               [7,0,0,0,0,2,9,4,0],
               [5,0,8,4,0,0,0,9,0],
               [0,0,2,8,0,0,0,0,0],
               [0,0,0,0,0,0,4,0,0]]
    
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

    board2=[[3,0,0,0,0,0,2,0,5],
       [5,0,6,0,0,0,0,0,0],
       [2,0,8,0,0,0,0,0,0],
       [4,0,0,0,0,5,0,0,6],
       [0,0,0,1,0,6,5,0,0],
       [0,0,0,0,0,0,0,0,9],
       [0,0,2,8,0,0,0,9,0],
       [0,0,0,0,0,7,0,0,4],
       [1,0,0,4,0,2,3,0,0]]

    solver.ajoutSudoku(board2)
    grid = solver.ajouterSudoku()
    solver.ajoutSudoku(grid)
    solver.printSudoku()
    print('\n\n')
    solver.InitPossi()
    print('\n\n')
    solver.solve2()
    solver.printSudoku()