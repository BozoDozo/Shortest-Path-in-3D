
def voisin_dijkstra(matrice: list, i: int, j: int ) -> list:
    """
    Renvoie la liste des voisins d'un élément dans une matrice pour
    l'algorithme de Dijkstra
    """
    liste_voisin = []
    #On regarde les voisins directs à gauche et à droite
    if(j_suiv := (j != len(matrice[0])-1)):
        liste_voisin.append(matrice[i][j+1])
    if(j_prec := (j != 0)):
        liste_voisin.append(matrice[i][j-1])
    #On regarde les voisins sur la ligne du dessus
    if i != 0:
        liste_voisin.append(matrice[i-1][j])
        if j_suiv:
            liste_voisin.append(matrice[i-1][j+1])
        if j_prec:
            liste_voisin.append(matrice[i-1][j-1])
    #On regarde les voisins sur la ligne du dessous
    if i != len(matrice) - 1:
        liste_voisin.append(matrice[i+1][j])
        if j_suiv:
            liste_voisin.append(matrice[i+1][j+1])
        if j_prec:
            liste_voisin.append(matrice[i+1][j-1])

    return liste_voisin

def dijkstra(matrice: list, depart: tuple,
                arrivee: tuple) -> list:
    """
    Renvoie la liste des points effectuant le plus court chemin entre
    un sommet de départ et sommet arrivée dansune matrice de coûts
    (déplacements: horizontaux, verticaux, diagonaux)
    avec l'algorithme de Dijkstra
    """
    #On itinialise la matrice de coûts cummulés tous les sommets à
    #la valeur infini l'élément de gauche est le coût,
    #l'élément de droite est le sommet precédent au sommet courant
    matrice_cout_cumul = [[[float('inf'),depart]
            for x in range(len(matrice[0]))] for y in range (len(matrice))]

    #On initialise le couple pour le sommet de départ
    matrice_cout_cumul[depart[0]][depart[1]] = (0, 0)
    #On part du sommet de départ
    courant = depart
    #Tant que l'on ne trouve pas l'arrivée
    while courant != arrivee:
        #On calcules les voisins du sommet courant
        liste_voisin = voisin_dijkstra(matrice,*courant)
        for voisin in liste_voisin:
