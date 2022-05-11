

"""

exemple une map de forme
  1 2 3
  4 5 6
  7 8 9
il nous faut la matrice de cout
on a aussi une matrice de liste_court avec les infini
et une liste voisin
"""


def liste_coor_djikstra(liste):
    liste_coord = []
    for i in range(len(liste)):

        x = liste[i]//10
        y = liste[i] % 10
        liste_coord.append((x, y))

    return liste_coord


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

    # Point d'intersection haut
    diag_haut_x = i - rayon
    if(diag_haut_x < 0):
        diag_haut_x = 0

    diag_haut_y = j + rayon
    if(diag_haut_y >= n):
        diag_haut_y = n-1

    # Point d'intersection bas
    diag_bas_x = i + rayon
    if(diag_bas_x >= n):
        diag_bas_x = n-1

    diag_bas_y = j - rayon
    if(diag_bas_y < 0):
        diag_bas_y = 0

    # On parcours de gauche à droite puis de haut en bas le quadrilatère
    # formé par les deux points d'intersections
    for k in range(diag_bas_y, diag_haut_y+1):
        for l in range(diag_haut_x, diag_bas_x+1):

            vec.append([k, l])

    return vec


def cree_liste(n, somde):
    liste = []

    for i in range(n):
        ligne = []
        for j in range(n):
            if i == somde[1] and j == somde[1]:
                ligne.append([-1, -1])
            else:
                ligne.append([float('inf'), 0])
        liste.append(ligne)
    return liste


def djikstraa(matrice, somde, somear):
    """
    matrice:liste de cout :liste de liste
    liste_square_map_id: liste de liste des carre
    depart:case de depart
    arrive:case d'arrive
    """

    save_somde = somde

    n = len(matrice)

    # liste=|0,inf,inf,inf]
    liste_court = cree_liste(n, somde)

    # changer depart
    somde = list(somde)
    a = somde[1]
    somde[1] = somde[0]
    somde[0] = a

    somear = list(somear)
    a = somear[1]
    somear[1] = somear[0]
    somear[0] = a
    # -----------------
    val = 0
    cpt = 0

    # boucle tant que on le chemin le plus court n'est pas arrive au point de depart
    while somde != somear:
        x_som = somde[1]
        y_som = somde[0]

        # liste des voisins de somde
        liste_voisin = clipping_voisin(matrice, x_som, y_som, rayon=1)

        # pour ne plus allé sur le sommet
        liste_court[y_som][x_som][0] = -1

        for voisin in liste_voisin:

            # on cherche le cout du voisin
            x = voisin[1]
            y = voisin[0]
            val_voisin = matrice[y][x]

            # pour passer par le chemin on teste
            if liste_court[y][x][0] > val_voisin+val:

                liste_court[y][x][0] = val_voisin+val

                liste_court[y][x][1] = somde

        # chercher le chemin le plus court
        save = float('inf')
        cpt_j = 0

        for j in liste_court:
            cpt_i = 0
            for i in j:
                if i[0] < save and i[0] > 0:
                    save = i[0]
                    somde = [cpt_j, cpt_i]
                cpt_i = cpt_i+1
            cpt_j = cpt_j+1
        # valeur du chemin pour additionner
        val = liste_court[somde[1]][somde[0]][0]

    # faire liste
    liste_chemin = []
    liste_chemin.append(somear)
    while somear != save_somde:

        if liste_court[somear[0]][somear[1]][1] == 0:
            break
        liste_chemin.append(liste_court[somear[0]][somear[1]][1])
        somear = liste_court[somear[0]][somear[1]][1]

    return liste_chemin


def circle_to_oval(x: int, y: int, r: int):
    return (x-r, y-r, x+r, y+r)


def tracer_dijkstra(liste, Canva):
    cote = 50
    for point in liste:
        i = point[1]
        j = point[0]
        xy_xy = circle_to_oval(i*cote+cote/2, j*cote+cote/2, 0.25*cote)
        depart_id = Canva.create_oval(*xy_xy, fill="green")
        Canva.itemconfigure(id, fill="blue")
