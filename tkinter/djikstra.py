"""

exemple une map de forme
  1 2 3
  4 5 6
  7 8 9
il nous faut la matrice de cout
on a aussi une matrice de liste_court avec les infini
et une liste voisin
"""


def clipping_voisin(matrice, i, j, rayon=1):
    """
    Clipping voisin d'un point avec un rayon carré
    --------------
    |     _______o_____
    |     | o    |    |
    |     |(i,j) |    |
    ------o-------    |
          |___________|
    Le point courant definit un carré autour de lui,
    trouver les points d'intersections
    Cas idéal pas d'intersection
    point haut : (i-rayon, j+rayon)
    point bas : (i+rayon, j-rayon)
    """
    n = len(matrice)
    vec = []

    #Point d'intersection haut
    diag_haut_x = i - rayon
    if(diag_haut_x < 0):
        diag_haut_x = 0

    diag_haut_y = j + rayon
    if(diag_haut_y >= n):
        diag_haut_y = n-1


    #Point d'intersection bas
    diag_bas_x = i + rayon
    if(diag_bas_x >= n):
        diag_bas_x = n-1

    diag_bas_y = j - rayon
    if(diag_bas_y < 0):
        diag_bas_y = 0

    #On parcours de gauche à droite puis de haut en bas le quadrilatère
    #formé par les deux points d'intersections


    for k in range(diag_haut_x, diag_bas_x+1):
        for l in range(diag_bas_y, diag_haut_y+1):

                vec.append(matrice[k][l])


    return vec

def cree_liste(n,somde):
    liste=[]
    # n*n car le cout ne peut etre plus grand
    #en vrai c'est un peu faut mais jai idee en tete
    for i in range(n*n):
            if i==somde:
                liste.append([-1,-1])
            else:
                liste.append([float('inf'),0])
    return liste

def djikstra(matrice,liste_square_map,somde,somear):
    """
    matrice:liste de cout :liste de liste
    liste_square_map_id: liste de liste des carre
    depart:case de depart
    arrive:case d'arrive
    """
    save_somde=somde

    n=len(matrice)

    #liste=|0,inf,inf,inf]
    liste_court=cree_liste(n,somde)


    #-----------------
    val=0
    cpt=0

    #boucle tant que on le chemin le plus court n'est pas arrive au point de depart
    while somde!=somear:
            x=somde//n
            y=somde %n

            ##liste des voisins de somde
            liste_voisin=clipping_voisin(liste_square_map, x,y, rayon=1)

            #pour ne plus allé sur le sommet
            liste_court[somde][0]=-1

            for voisin in liste_voisin:
                #on cherche le cout du voisin
                voisin=voisin-1
                x=voisin//n
                y=voisin%n
                val_voisin=matrice[x][y]
                if val_voisin>=15:
                    val_voisin=float('inf')
                #pour passer par le chemin on teste
                if liste_court[voisin][0]>val_voisin+val:
                    liste_court[voisin][0]=val_voisin+val
                    liste_court[voisin][1]=somde



            #chercher le chemin le plus court
            save=float('inf')
            cpt=0
            for i in liste_court:
                if i[0] <save and i[0]>0:

                    save=i[0]
                    somde=cpt
                cpt=cpt+1
            #valeur du chemin pour additionner
            val=liste_court[somde][0]

    #faire liste
    liste_chemin=[]
    liste_chemin.append(somear)
    while somear!=save_somde:

        liste_chemin.append(liste_court[somear][1])
        somear=liste_court[somear][1]

    return liste_chemin

def tracer_dijkstra(liste,canva):
    for id in liste:
        canva.itemconfigure(id,fill="blue")
