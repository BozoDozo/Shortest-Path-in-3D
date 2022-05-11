from math import sqrt


def faire_voisin(somde):
    n = len(matrice)
    liste_voisin = ()
    numero_poly = somde
    i = somde//n
    j = somde % n

    # premier ligne de la map
    if i == 0 and j == 0:
        liste_voisin = (numero_poly+1, numero_poly+n, numero_poly+n+1)
    elif i == 0 and j == n-1:
        liste_voisin = (numero_poly-1, numero_poly+n, numero_poly+n-1)
    elif i == 0:
        liste_voisin = (numero_poly-1, numero_poly+1,
                        numero_poly+n, numero_poly+n+1, numero_poly+n-1)
        # dernier ligne de la map
    elif i == n-1 and j == 0:
        liste_voisin = (numero_poly+1, numero_poly-n, numero_poly-n+1)
    elif i == n-1 and j == n-1:
        liste_voisin = (numero_poly-1, numero_poly-n, numero_poly-n-1)
    elif i == n-1:
        liste_voisin = (numero_poly-1, numero_poly+1,
                        numero_poly-n, numero_poly-n+1, numero_poly-n-1)
        # le cote gauche
    elif j == 0:
        liste_voisin = (numero_poly+1, numero_poly-n,
                        numero_poly+n, numero_poly+n+1, numero_poly-n+1)
        # le cote droit
    elif j == n-1:
        liste_voisin = (numero_poly-1, numero_poly-n,
                        numero_poly+n, numero_poly+n-1, numero_poly-n-1)
        # le millieux
    else:
        liste_voisin = (numero_poly-1, numero_poly+1, numero_poly-n, numero_poly+n,
                        numero_poly-n-1, numero_poly-n+1, numero_poly+n-1, numero_poly+n+1)
    return liste_voisin


def cree_liste(n, somde):
    liste = []
    # n*n car le cout ne peut etre plus grand
    # en vrai c'est un peu faut mais jai idee en tete
    for i in range(n*n):
        if i == somde:
            liste.append([-1, -1])
        else:
            liste.append([float('inf'), 0])
    return liste


def coutdistance(xa, ya, xb, yb):
    X = xb-xa
    Y = yb-ya
    X = X*X
    Y = Y*Y
    return sqrt(X+Y)


def astar(matrice, somde, somear):
    # matrice de cout,sommde= sommet de depart,sommear au sommet arrivé
    # en sortie on aura une liste du plus court chemin
    save_somde = somde

    n = len(matrice)
    # liste des voisins de somde
    liste_voisin = faire_voisin(somde)
    # liste=|0,inf,inf,inf]
    liste_court = cree_liste(n, somde)
    # -----------------
    val = 0

    # boucle tant que on le chemin le plus court n'est pas arrive au point de depart
    while somde != somear:

        # liste des voisins de somde
        liste_voisin = faire_voisin(somde)
        # pour ne plus allé sur le sommet
        liste_court[somde][0] = -1
        for voisin in liste_voisin:
            # on cherche le cout du voisin
            x = voisin//n
            y = voisin % n
            xa = somde//n
            ya = somde % n
            val_voisin = matrice[x][y]+coutdistance(xa, ya, x, y)
            # pour passer par le chemin on teste
            if liste_court[voisin][0] > val_voisin+val:
                liste_court[voisin][0] = val_voisin+val
                liste_court[voisin][1] = somde
             # chercher le chemin le plus court
        save = float('inf')
        cpt = 0
        for i in liste_court:
            if i[0] < save and i[0] > 0:

                save = i[0]
                somde = cpt
            cpt = cpt+1
        # valeur du chemin pour additionner
        val = liste_court[somde][0]

    # faire liste
    liste_chemin = []
    liste_chemin.append(somear)
    while somear != save_somde:

        liste_chemin.append(liste_court[somear][1])
        somear = liste_court[somear][1]
    print(liste_chemin)


matrice = [[7, 2, 4], [3, 8, 8], [1, 4, 5]]
astar(matrice, 3, 8)
