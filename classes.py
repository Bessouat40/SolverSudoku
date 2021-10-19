import numpy as np

class Solver:
    def __init__(self, sudoku = [[0 for i in range(9)]for i in range(9)]) : 
        self.sudoku = sudoku
        self.possibilite = [[[i for i in range(1,10)]for i in range(9)] for i in range(9)]

    def getSudoku(self) :
        return self.sudoku

    def getPossibilites(self) :
        return self.possibilite

    def getCarre(self, i) :
        indices = [i*3, i*3+1, i*3+2]
        carre = []
        sudoku = self.getPossibilites()
        for j in indices :
            ligne = sudoku[j][i*3:i*3+3]
            carre.append(ligne)
        return carre

    def printSudoku(self) :
        for i in self.getSudoku() :
            print('---'*9)
            for j in i :
                print('|'+str(j)+'|', end="")
            print("")
        print('---'*9)

    def printPossibilites(self) :
        for i in self.getPossibilites() :
            print(i)
        print('\n')

    def verifLigne(self, i) :
        ligne = self.getSudoku()[i]
        verif = [i for i in range(1,10)]
        return sorted(verif) == sorted(ligne)

    def verifColonne(self, i) :
        colonne = np.array(self.getSudoku())[:,i]        
        verif = [i for i in range(1,10)]
        return sorted(verif) == sorted(colonne)
    
    def verifCarre(self, i) :
        indices = [i*3, i*3+1, i*3+2]
        verif = [i for i in range(1,10)]
        carre = []
        sudoku = self.getSudoku()
        for j in indices :
            ligne = sudoku[j][i*3:i*3+3]
            carre.append(ligne)
        carre = np.asarray(carre).flatten()

        return sorted(verif) == sorted(carre)

    def ajoutSudoku(self, sudoku) :
        if len(sudoku) != 9 or len(sudoku[0]) != 9 :
            print("La taille du sodoku n'est pas conforme. Veuillez rentrer une grille de taille 9x9.")        
        else : self.sudoku = sudoku

    def modifPossiLigne(self, val, ligne, pos) :
        possi = self.getPossibilites()[ligne]
        for i in range(len(possi)) :
            if i == pos : None
            else :
                x = possi[i]
                x[val-1] = 0 # val-1 car on commence à 0
                possi[i] = x
        self.possibilite[ligne] = possi

    def modifPossiCol(self, val, col, pos) :
        possi = np.asarray(self.getPossibilites())[:,col]
        for i in range(len(possi)) :
            if i == pos : None
            else :
                x = possi[i]
                x[val-1] = 0 # val-1 car on commence à 0
                possi[i] = x
        for count, val in enumerate(self.possibilite) :
            val[col] = list(possi[count])

    def modifPossiCarre(self, val, num_carre, pos) :
        carre = np.array(self.getCarre(num_carre))
        indices = [num_carre*3, num_carre*3+1, num_carre*3+2]
        for i in range(len(carre)) :
            for j in range(len(carre[0])) :
                if [i,j] == pos : None 
                else : 
                    carre[i,j][val-1] = 0
                carre[i,j] = list(carre[i,j])
        for i, j in enumerate(indices) :
            self.possibilite[j][num_carre*3:num_carre*3+3] = list(carre[i])
        

if __name__ == "__main__":

    solver = Solver()
    grille = [[0,4,0,1,0,0,0,0,0], 
              [0,0,3,5,0,0,0,1,9],
              [0,0,0,0,0,6,0,0,3],
              [0,0,7,0,0,5,0,0,8],
              [0,8,1,0,0,0,9,6,0],
              [9,0,0,2,0,0,7,0,0],
              [6,0,0,9,0,0,0,0,0],
              [8,1,0,0,0,2,4,0,0],
              [0,0,0,0,0,4,0,9,0]]
    sudoku = [[i for i in range(1,10)] for i in range(1,10)]
    solver.ajoutSudoku(sudoku)
    solver.printSudoku()
    print('\n')
    print('ligne 1 : ' + str(solver.verifLigne(1)))
    print('colonne 1 : ' + str(solver.verifColonne(1)))
    print('carre 1 : ' + str(solver.verifCarre(1)))
    print('possibilites : ' )
    solver.modifPossiCarre(1,0,[0,0])
    print(solver.possibilite)