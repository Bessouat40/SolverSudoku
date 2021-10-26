import numpy as np


class Solver:
    def __init__(self, sudoku=[[0 for i in range(9)] for i in range(9)]):
        self.sudoku = sudoku
        self.possibilite = [[[1 for i in range(1, 10)] for i in range(9)] for i in range(9)]

    def InitPossi(self) :
        for i in range(len(self.sudoku)) :
            for j in range(len(self.sudoku[0])) :
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
        x = (n2 % 3) * 3
        y = (n2 // 3) * 3
        indices = [[x + i, y + j] for i in range(3) for j in range(3)]
        return indices

    def zero_sudo(self) :
        pos = []
        for i in range(self.sudoku) :
            for j in range(self.sudoku[0]) :
                if self.sudoku[i,j] == 0 :
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
        # Vérifier si la ligne a tous les numéros
        ligne = self.getSudoku()[i]
        verif = [i for i in range(1, 10)]
        return sorted(verif) == sorted(ligne)

    def verifColonne(self, i):
        # Vérifier si la colonne a tous les numéros
        colonne = np.array(self.getSudoku())[:, i]
        verif = [i for i in range(1, 10)]
        return sorted(verif) == sorted(colonne)

    def verifCarre(self, i):
        # Vérifier si le carré a tous les numéros
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

    def modifPossiLigne(self, ligne, val):
        # On modofie les posisbilité de la ligne en fonction de la valeur posée
        possi = self.getPossibilites()[ligne]
        for i in range(len(possi)):
            x = possi[i]
            x[val - 1] = 0  # val-1 car on commence à 0
            possi[i] = x
        self.possibilite[ligne] = possi

    def modifPossiCol(self, col, val):
        possi = np.asarray(self.getPossibilites())[:, col]
        for i in range(len(possi)):
            x = possi[i]
            x[val - 1] = 0  # val-1 car on commence à 0
            possi[i] = x
            self.possibilite[i][col][val-1]=0
        # for count, val in enumerate(self.possibilite):
        #     val[col] = list(possi[count])

    def retrouveCarre(self, x, y):
        carre = (y // 3) * 3 + 1 + x // 3
        return carre

    def posCarre(self, nb_carre):
        x = ((nb_carre - 1)%3)*3
        y = (((nb_carre-1)//3))*3
        return x,y

    def modifPossiCarre(self, pos, val):
        num_carre = self.retrouveCarre(pos[0], pos[1])
        carre = self.getCarre(num_carre)
        indice = self.getIndicesCarre(num_carre)
        for i in range (len(carre)) :
            carre[i][val-1]=0
        for j in range (len(carre)) :
            self.possibilite[indice[j][1]][indice[j][0]]=carre[j]

    def sommerValeursPossibles(self):
        return np.sum(self.possibilite, axis=1)

    def compterZeroSudoku(self, m):
        nb_zeros = len(np.where(m == 0)[0])
        return nb_zeros

    def acTrois(self):
        None

    def mrv(self):
        liste = self.possibilite
        min = [10]
        position = [[0, 0]]
        for i in range(len(liste)):
            for j in range(len(liste)):
                if np.sum(liste[i][j]) < min and np.sum(liste[i][j]) > 0:
                    min = np.sum(liste[i][j])
                    position = [[i,j]]
                elif np.sum(liste[i][j]) == min and np.sum(liste[i][j]) > 0:
                    min.append(np.sum(liste[i][j]))
                    position.append([i,j])
        return position

    def AC3(self, pos, val) :
        self.modifPossiLigne(pos[0], val)
        self.modifPossiCol(pos[1], val)
        self.modifPossiCarre(pos, val)

    def compterZeroLigne(self, ligne):
        # On compte le nombre de case dans une ligne où il est impossible de rentrer une valeur
        possi = self.possibilite[ligne]
        compte = 0
        for k in range(len(possi)):
            if possi[k].count(0) == 9:
                compte += 1
        return compte

    def compterZeroColonne(self, col):
        possi = self.possibilite[:,col]
        print(possi)
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
        # On compte le nombre de possibilité dans un carré
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
        carre = np.array(self.getCarre(num_carre))
        for i in range(len(carre)):
            for j in i :
                s += sum(j)                    
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


    def degreeHeuristic(self):
        # A TESTER
        nbre_contrainte = [[0 for i in range(9)] for i in range(9)]
        for i in range(len(self.sudoku)):
            for j in range(len(self.sudoku)):
                num_carre = self.retrouveCarre(i, j)
                # PROBLEME PAR LA A MON AVIS
                calcul_contrainte = self.compterZeroColonne(j) + self.compterPZeroLigne(i)
                calcul_contrainte += self.sommerZeroCarre(num_carre)
                calcul_contrainte += -8 * 3 - np.sum(self.possibilite[i][j])
                calcul_contrainte += self.sommerPossiLigne(i) + self.sommerPossiCol(j) + self.sommerPossiCarre(
                    num_carre)
                nbre_contrainte[i][j] = calcul_contrainte
        return self.indiceMin(nbre_contrainte)

    def leastConstraining(self):
        # A TESTER
        nbre_contrainte = [[0 for i in range(9)] for i in range(9)]
        for i in range(len(self.sudoku)):
            for j in range(len(self.sudoku)):
                num_carre = self.retrouveCarre(i, j)
                # PROBLEME PAR LA A MON AVIS
                calcul_contrainte = self.compterZeroColonne(j) + self.compterPZeroLigne(i)
                calcul_contrainte += self.sommerZeroCarre(num_carre)
                calcul_contrainte += -8 * 3 - np.sum(self.possibilite[i][j])
                calcul_contrainte += self.sommerPossiLigne(i) + self.sommerPossiCol(j) + self.sommerPossiCarre(
                    num_carre)
                nbre_contrainte[i][j] = calcul_contrainte
        return self.indiceMax(nbre_contrainte)


if __name__ == "__main__":
    solver = Solver()
    grille = [[0, 4, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 3, 5, 0, 0, 0, 1, 9],
              [0, 0, 0, 0, 0, 6, 0, 0, 3],
              [0, 0, 7, 0, 0, 5, 0, 0, 8],
              [0, 8, 1, 0, 0, 0, 9, 6, 0],
              [9, 0, 0, 2, 0, 0, 7, 0, 0],
              [6, 0, 0, 9, 0, 0, 0, 0, 0],
              [8, 1, 0, 0, 0, 2, 4, 0, 0],
              [0, 0, 0, 0, 0, 4, 0, 9, 0]]

    sudoku = [[i for i in range(1, 10)] for i in range(1, 10)]
    solver.ajoutSudoku(grille)
    solver.printSudoku()
    print('\n\n')
    #solver.modifPossiCarre(8, [4, 4])
    #solver.printPossibilites()
    """print('ligne 1 : ' + str(solver.verifLigne(1)))
    print('colonne 1 : ' + str(solver.verifColonne(1)))
    print('carre 1 : ' + str(solver.verifCarre(1)))
    print('possibilites : ')    
    print(solver.possibilite)
    print(solver.sommerValeursPossibles())"""
    solver.InitPossi()
    print(solver.possibilite[4][3])
    solver.printPossibilites()