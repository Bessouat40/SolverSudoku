import numpy as np


class Solver:
    def __init__(self, sudoku=[[0 for i in range(9)] for i in range(9)]):
        self.sudoku = sudoku
        self.possibilite = [[[1 for i in range(1, 10)] for i in range(9)] for i in range(9)]

    def getSudoku(self):
        return self.sudoku

    def getPossibilites(self):
        return self.possibilite

    def getCarre(self, i):
        indices = [i * 3, i * 3 + 1, i * 3 + 2]
        carre = []
        sudoku = self.getPossibilites()
        for j in indices:
            ligne = sudoku[j][i * 3:i * 3 + 3]
            carre.append(ligne)
        return carre

    def printSudoku(self):
        for i in self.getSudoku():
            print('---' * 9)
            for j in i:
                print('|' + str(j) + '|', end="")
            print("")
        print('---' * 9)

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

    def modifPossiLigne(self, val, ligne, pos):
        # On modofie les posisbilité de la ligne en fonction de la valeur posée
        possi = self.getPossibilites()[ligne]
        for i in range(len(possi)):
            x = possi[i]
            x[val - 1] = 0  # val-1 car on commence à 0
            possi[i] = x
        self.possibilite[ligne] = possi

    def modifPossiCol(self, val, col, pos):
        possi = np.asarray(self.getPossibilites())[:, col]
        for i in range(len(possi)):
            x = possi[i]
            x[val - 1] = 0  # val-1 car on commence à 0
            possi[i] = x
        for count, val in enumerate(self.possibilite):
            val[col] = list(possi[count])

    def retrouveCarre(self, x, y):
        carre = (y // 3) * 3 + 1 + x // 3
        return carre

    def posCarre(self, nb_carre):
        x = ((nb_carre - 1)%3)*3
        y = (((nb_carre-1)//3))*3
        return x,y

    def modifPossiCarre(self, val, num_carre, pos):
        carre = np.array(self.getCarre(num_carre))
        indices = [num_carre * 3, num_carre * 3 + 1, num_carre * 3 + 2]
        for i in range(len(carre)):
            for j in range(len(carre[0])):
                carre[i, j][val - 1] = 0
                carre[i, j] = list(carre[i, j])
        for i, j in enumerate(indices):
            self.possibilite[j][num_carre * 3:num_carre * 3 + 3] = list(carre[i])

    def miseAJour(self, val, position):
        self.modifPossiCarre(val, self.retrouveCarre(position), self.possibilite)
        self.modifPossiLigne(val, position[1], self.possibilite)
        self.modifPossiCol(val, position[2], self.possibilite)

    def sommerValeursPossibles(self):
        return np.sum(self.possibilite, axis=1)

    def compterZeroSudoku(self, m):
        nb_zeros = len(np.where(m == 0)[0])
        return nb_zeros

    def acTrois(self):
        None

    def mrv(self):
        liste = self.possibilite
        min = 10
        position = [0, 0]
        for i in range(len(liste)):
            for j in range(len(liste)):
                if np.sum(liste[i][j]) < min and np.sum(liste[i][j]) > 0:
                    min = np.sum(liste[i][j])
                    position[0] = i
                    position[1] = j
        return position

        """    def mrv(self):
        liste = self.sommerValeursPossibles()
        zero_possi = self.compterZeroSudoku(self.sommerValeursPossibles())
        zero_sudo = self.compterZeroSudoku(self.sudoku)
        while zero_possi > 0 and zero_sudo > 0 :
            position = self.rechercheMin(liste)
            
            #self.sudoku[position[0]][position[1]] = np.nonzero(self.possibilite[position[0]][position[1]])[0][0])"""

    def compterPossibiliteZeroLigne(self, ligne):
        # On compte le nombre de case dans une ligne où il est impossible de rentrer une valeur
        possi = self.possibilite[ligne]
        compte = 0
        for k in range(len(possi)):
            if possi[k].count(0) == 9:
                compte += 1
        return compte

    def compterZeroColonne(self, col):
        possi = np.asarray(self.getPossibilites())[:, col]
        compte = 0
        for k in range(len(possi)):
            if possi[k].count(0) == 9:
                compte += 1
        return compte

    def compterZeroCarre(self, num_carre):
        carre = np.array(self.getCarre(num_carre))
        compte = 0
        for i in range(len(carre)):
            if carre[i].count(0) == 9:
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
        x,y = self.posCarre(num_carre)
        for i in range(3):
            for j in range(3):
                s+=np.sum(self.possibilite[y+i,x+j])
        return s


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
        return np.argmin(nbre_contrainte)

    def leastConstraining(self):
        None


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
    solver.ajoutSudoku(sudoku)
    solver.printSudoku()
    print('\n')
    print('ligne 1 : ' + str(solver.verifLigne(1)))
    print('colonne 1 : ' + str(solver.verifColonne(1)))
    print('carre 1 : ' + str(solver.verifCarre(1)))
    print('possibilites : ')
    solver.modifPossiCarre(1, 0, [0, 0])
    print(solver.possibilite)

    print(solver.sommerValeursPossibles())
