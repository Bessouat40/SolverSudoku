import numpy as np

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap

class Solver:

    def __init__(self, sudoku=[[0 for i in range(9)] for i in range(9)]):
        self.sudoku = sudoku

    def ajouterSudoku(self):
        print("\n Veuillez entrer le sudoku ligne par ligne en séparant les chiffres par des virgules")
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

    def displaySudoku(self, grid):
        cmap = ListedColormap(['w'])
        fig, ax = plt.subplots()
        # Using matshow here just because it sets the ticks up nicely. imshow is faster.
        ax.matshow(grid, cmap=cmap)

        for (i, j), z in np.ndenumerate(grid):
            ax.text(j, i, z, ha='center', va='center')
        c1 = [[(.5 + k, -3), (.5 + k, 9)] for k in range(11)]
        c2 = [[(-3, .5 + k), (9, .5 + k)] for k in range(11)]
        colec = c1 + c2
        lc = LineCollection(colec, color=["k"], lw=1)
        c1 = [[(-3.5 + 3*k, -3), (-3.5 + 3*k, 9)] for k in range(4)]
        c2 = [[(-3, -3.5 + 3*k), (9, -3.5 + 3*k)] for k in range(4)]
        colec2 = c1+c2
        lc2 = LineCollection(colec2, color=["k"], lw=2)
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.set_xticks([])
        ax.set_yticks([])
        plt.gca().add_collection(lc)
        plt.gca().add_collection(lc2)
        plt.show()

    def getSudoku(self):
        return self.sudoku

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

    def ajoutSudoku(self, sudoku):
        if len(sudoku) != 9 or len(sudoku[0]) != 9:
            print("La taille du sodoku n'est pas conforme. Veuillez rentrer une grille de taille 9x9.")
        else:
            self.sudoku = sudoku

    def retrouveCarre(self, x, y):
        ligne = [[1,2,3], [4,5,6], [7,8,9]]
        colonne = [[1,4,7], [2,5,8], [3,6,9]]
        comm = list(set(ligne[x//3]).intersection(colonne[y//3]))[0]
        return comm

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

    def Backtracking(self) :
        find = self.zero_sudo()
        if len(find) == 0 :
            return True
        else : 
            l = self.mrv(find) 
            if len(l) != 0 :
                l = self.degreeHeuristic(l)
            row, col = l[0]
        for i in range(1,10):
            if self.possible([row,col],i) :
                self.sudoku[row][col] = i
                if self.Backtracking() :
                    return True
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

    print('\n Voulez vous ajouter votre sudoku ? Oui/Non')
    reponse = input()
    if reponse == 'Oui' :
        grid = solver.ajouterSudoku()
        solver.ajoutSudoku(grid)
    else :
        solver.ajoutSudoku(board2)
        print('\n Voici notre grille par défaut :')
    print('\n\n ----------Sudoku initial----------\n ')
    solver.printSudoku()
    solver.Backtracking()
    print('\n\n -----------Sudoku final-----------\n ')
    solver.printSudoku()
    solver.displaySudoku(solver.sudoku)