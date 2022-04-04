from map import clipping_voisin

def init_dijkstra(n, depart):
    """
    Créé la matrice de coût déroulé
    chaque élément possède un couple
    le coût et le sommet précédent
    """
    #On itinialise tous les sommets à la valeur infini
    liste_cout = [[[float('inf'),depart] for x in range(n)] for y in range (n)]

    #On initialise le couple pour le sommet de départ
    liste_cout[depart[0]][depart[1]] = [0, -1]


def dijkstra(matrice, depart, arrivee):

    #On itinialise tous les sommets à la valeur infini
    liste_cout = [[[float('inf'),depart] for x in range(n)] for y in range (n)]

    #On initialise le couple pour le sommet de départ
    liste_cout[depart[0]][depart[1]] = [0, -1]

    courant = depart

    while courant != arrivee:

        #On met les voisins dans une liste
        liste_voisin = clipping_voisin(matrice, courant[0], courant[1])

        #On indique que l'on est déjà passé par ici
        liste_cout[courant[0]][courant[1]][1] =
