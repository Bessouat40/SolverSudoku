import numpy as np
import sys

class Solver:
    def __init__(self, sudoku=[[0 for i in range(9)] for i in range(9)]):
        self.sudoku = sudoku
        self.possibilite = [[[1 for i in range(1, 10)] for i in range(9)] for i in range(9)]
        self.count = 0
        self.fixe = [[] for i in range(9)]

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

    def verifLigne(self, i):
        # V??rifier si la ligne a tous les num??ros
        ligne = self.getSudoku()[i]
        verif = [i for i in range(1, 10)]
        return sorted(verif) == sorted(ligne)

    def verifColonne(self, i):
        # V??rifier si la colonne a tous les num??ros
        colonne = np.array(self.getSudoku())[:, i]
        verif = [i for i in range(1, 10)]
        return sorted(verif) == sorted(colonne)

    def verifCarre(self, i):
        # V??rifier si le carr?? a tous les num??ros
        indices = [i * 3, i * 3 + 1, i * 3 + 2]
        verif = [i for i in range(1, 10)]
        carre = []
        sudoku = self.getSudoku()
        for j in indices:
            ligne = sudoku[j][i * 3:i * 3 + 3]
            carre.append(ligne)
        carre = np.asarray(carre).flatten()

        return sorted(verif) == sorted(carre)

    def ajoutSudoku(self, sudoku):
        if len(sudoku) != 9 or len(sudoku[0]) != 9:
            print("La taille du sodoku n'est pas conforme. Veuillez rentrer une grille de taille 9x9.")
        else:
            self.sudoku = sudoku

    def modifPossiLigne(self, ligne, val, remp):
        # On modofie les posisbilit?? de la ligne en fonction de la valeur pos??e
        possi = self.possibilite[ligne]
        for i in range(len(possi)):
            x = possi[i]
            x[val - 1] = remp  # val-1 car on commence ?? 0
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

    def sommerValeursPossibles(self):
        return np.sum(self.possibilite, axis=1)

    def compterZeroSudoku(self, m):
        nb_zeros = len(np.where(m == 0)[0])
        return nb_zeros

    def mrv(self, arg):
            min = 10000
            position = []
            for i in arg:
                sum_possi = np.sum(self.possibilite[i[0]][i[1]])
                if sum_possi < min and sum_possi > 0:
                    min = sum_possi
                    position = [i]
                elif sum_possi == min and sum_possi > 0:
                    position.append(i)
            return position

    def AC3(self, pos, val) :
        self.modifPossiLigne(pos[0], val, 0)
        self.modifPossiCol(pos[1], val, 0)
        self.modifPossiCarre(pos, val, 0)

    def InvAC3(self, pos, val) :
        self.modifPossiLigne(pos[0], val, 1)
        self.modifPossiCol(pos[1], val, 1)
        self.modifPossiCarre(pos, val, 1)
        for i in range(len(self.sudoku)) :
            for j in range(len(self.sudoku[0])) :
                if self.fixe[i][j] != 0 :
                    self.possibilite[i][j] = [0 for i in range(9)]



    def compterZeroLigne(self, ligne):
        # On compte le nombre de case dans une ligne o?? il est impossible de rentrer une valeur
        possi = self.possibilite[ligne]
        compte = 0
        for k in range(len(possi)):
            if possi[k].count(0) == 9:
                compte += 1
        return compte

    def compterZeroColonne(self, col):
        possi = self.possibilite[:][col]
        compte = 0
        for k in range(len(possi)):
            if possi[k].count(0) == 9:
                compte += 1
        return compte

    def compterZeroCarre(self, num_carre):
        carre = np.array(self.getCarre(num_carre))
        compte = 0
        for i in range(len(carre)):
            for j in i :
                if i.count(0) == 9:
                    compte += 1
        return compte

    def sommerZeroCarre(self, num_carre):
        # On compte le nombre de possibilit?? dans un carr??
        carre = np.array(self.getCarre(num_carre))
        compte = 0
        for i in range(len(carre)):
            compte += np.sum(carre[i])

        return compte

    def sommerPossiLigne(self, ligne):
        somme = 0
        for k in range(len(self.possibilite[ligne])):
            somme += np.sum(self.possibilite[ligne][k])

        return somme

    def sommerPossiCol(self, col):
        somme = 0
        for k in range(len(self.possibilite[col])):
            somme += np.sum(self.possibilite[k][col])

        return somme

    def sommerPossiCarre(self, num_carre):
        s = 0
        carre = self.getCarre(num_carre)
        for i in carre:
            s += sum(i)                    
        return s

    def indicesMax(self, tableau):
        max=np.max(tableau)
        position=[]
        for i in range(len(tableau)) :
            for j in range (len(tableau)):
                if max == tableau[i][j]:
                    position.append([i,j])
        return position

    def indicesMin(self, tableau):
        min=np.min(tableau)
        position=[]
        for i in range(len(tableau)) :
            for j in range (len(tableau)):
                if min == tableau[i][j]:
                    position.append([i,j])
        return position


    def degreeHeuristic(self, arg):
        # A TESTER
        nbre_contrainte = [[0 for i in range(9)] for i in range(9)]
        for k in range(len(arg)):
            i = arg[k][0]
            j=arg[k][1]
            num_carre = self.retrouveCarre(arg[k][0], arg[k][1])
            # PROBLEME PAR LA A MON AVIS
            calcul_contrainte = self.compterZeroColonne(j) + self.compterZeroLigne(i)
            calcul_contrainte += self.sommerZeroCarre(num_carre)
            calcul_contrainte += -8 * 3 - np.sum(self.possibilite[i][j])
            calcul_contrainte += self.sommerPossiLigne(i) + self.sommerPossiCol(j) + self.sommerPossiCarre(
                num_carre)
            nbre_contrainte[i][j] = calcul_contrainte
        return self.indicesMin(nbre_contrainte)

    def leastConstraining(self, arg):
        # A TESTER
        nbre_contrainte = [[0 for i in range(9)] for i in range(9)]
        for k in range(len(arg)):
            i = arg[k][0]
            j = arg[k][1]
            num_carre = self.retrouveCarre(i, j)
            # PROBLEME PAR LA A MON AVIS
            calcul_contrainte = self.compterZeroColonne(j) + self.compterZeroLigne(i)
            calcul_contrainte += self.sommerZeroCarre(num_carre)
            calcul_contrainte += -8 * 3 - np.sum(self.possibilite[i][j])
            calcul_contrainte += self.sommerPossiLigne(i) + self.sommerPossiCol(j) + self.sommerPossiCarre(num_carre)
            nbre_contrainte[i][j] = calcul_contrainte
        return self.indicesMax(nbre_contrainte)

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
            row, col = find[0]
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

    """def solve(self) :
        find = self.zero_sudo()
        if len(find) == 0 :
            print('finito pipo')
            return True
        else : 
            row, col = find[0]
        for i in range(1,10):
            possi = self.possibilite[row][col][i-1]
            if possi==1 :
                print('coucou')
                print(self.possibilite)
                self.sudoku[row][col] = i
                self.AC3([row,col],i)
                #self.printSudoku()
                if self.solve() :
                    return True
                else :
                    self.sudoku[row][col] = 0
                    self.InvAC3([row,col],i)
        return False"""


    def solve2(self) :
        find = self.zero_sudo()
        if len(find) == 0 :
            print('finito pipo')
            return True
        else : 
            row, col = find[0]
        for i in range(1,10):
            if self.possible([row,col],i) :
                self.sudoku[row][col] = i
                if self.solve2() :
                    return True
            self.sudoku[row][col] = 0
        return False

    def recu(self, pos) :
        for i in range(1,10) :
            if self.possibilite[pos[0]][pos[1]][i-1] == 1 :
                self.sudoku[pos[0]][pos[1]] = i
                self.AC3(pos, i)
                if self.Backtracking() :
                    print('fin recu')
                    self.printSudoku()
                    return True  
                
                self.sudoku[pos[0]][pos[1]] = 0
                self.InvAC3(pos, i)

    def Backtracking(self) :
        self.count += 1
        if self.count % 15000 == 0 :
            self.printSudoku()
            print(self.count)

        zeros = self.zero_sudo()
        if len(zeros) == 0 :
            print('finiiii')
            return True  

        else : 
            self.recu(zeros[0])

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

    solver.ajoutSudoku(grille)
    solver.printSudoku()
    print('\n\n')
    solver.InitPossi()
    print('\n\n')
    solver.solve()
    solver.printSudoku()