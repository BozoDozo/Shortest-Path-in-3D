from heapq import heappush, heappop
import numpy as np
from math import sqrt


# approximation de la racine de 2
sqr2 = 1.41
def distance_eucl(x0: float, y0: float, x1: float, y1: float):
    """
    Calcule la distance euclidienne entre 2 points
    """
    return sqrt((x1-x0)*(x1-x0)+(y1-y0)*(y1-y0))
def voisin_dijkstra(matrice: np.matrix, i: int, j: int ) -> list:
    """
    Renvoie la liste des voisins d'un élément de la matrice
    ainsi que leur coûts fixes
    """
    l, c = matrice.shape
    liste_voisin = []
    #On regarde les voisins directs à gauche et à droite
    if(j_suiv := (j != c-1)):
        liste_voisin.append((matrice[i,j+1],(i, j+1)))
    if(j_prec := (j != 0)):
        liste_voisin.append((matrice[i,j-1],(i, j-1)))
    #On regarde les voisins sur la ligne du dessus
    if i != 0:
        liste_voisin.append((matrice[i-1,j],(i-1, j)))
        if j_suiv:
            liste_voisin.append((matrice[i-1,j+1]*sqr2,(i-1, j+1)))
        if j_prec:
            liste_voisin.append((matrice[i-1,j-1]*sqr2,(i-1, j-1)))
    #On regarde les voisins sur la ligne du dessous
    if i != l - 1:
        liste_voisin.append((matrice[i+1,j],(i+1, j)))
        if j_suiv:
            liste_voisin.append((matrice[i+1,j+1],(i+1, j+1)))
        if j_prec:
            liste_voisin.append((matrice[i+1,j-1],(i+1, j-1)))

    return liste_voisin


# def relacher(debut: tuple, fin: tuple, cout_cum: np.):
#     if()
def dijkstra(matrice: np.matrix, depart: tuple,
                arrivee: tuple) -> list:
    """
    Renvoie la liste des points effectuant le plus court chemin entre
    un sommet de départ et sommet arrivée dansune matrice de coûts
    (déplacements: horizontaux, verticaux, diagonaux)
    avec l'algorithme de Dijkstra
    """
    matrice[arrivee] # Pour vérifier si l'arrivee est dans la matrice
    if(depart == arrivee): # le depart est il l'arrivee
        return [()]
    # Initialisation de la matrice de cout cummulee qui contient
    # la distance minimale pour aller a un sommet
    l, c = matrice.shape
    cout_cumul = np.matrix([[np.inf
            for y in range(c)] for x in range (l)])
    # tableau de precedence pour retrouver le chemin une fois
    # dijkstra fini
    prec = np.array([[(-1,-1)
            for y in range(c)] for x in range (l)], dtype=object)
    # On initialise le couple pour le sommet de départ
    cout_cumul[depart[0],depart[1]] = float(0)
    chemin = []
    # Tas minimal
    tas = []
    # Pour savoir par où on est passé
    visite = set()
    # Pour initaliser l'algo
    courant = depart
    cout = 0
    heappush(tas,(0,depart))
    # Tant que l'on ne trouve pas l'arrivée
    while courant != arrivee and tas != []:
        # On ajoute aux sommets visités le sommet courant
        if courant not in visite:
            visite.add(courant)
            # On détermine les voisins du sommet courant
            liste_voisin = voisin_dijkstra(matrice, *courant)
            # On parcours les voisins
            for voisin in liste_voisin:
                # On recupere les coordonnees et le cout du voisin
                voisin_cout, voisin_coords = voisin
                # On calcule le cout pour passer au voisin
                cout_suiv = voisin_cout + cout
                # Si le cout cumulé pour aller au voisin
                if(cout_cumul[voisin_coords] > cout_suiv):
                    heappush(tas, (cout_suiv, voisin_coords))
                    cout_cumul[voisin_coords] = cout_suiv
                    prec[voisin_coords] = courant
        # On recupere le prochain sommet avec un cout minimal
        cout, courant = heappop(tas)
    if tas == []:
        print("Pas de chemin")
        return [()]
    while(courant != depart):
        chemin.append(courant)
        courant = tuple(prec[courant])
    chemin.append(depart)
    chemin.reverse()
    return chemin

def a_star(matrice: np.matrix, depart: tuple,
                arrivee: tuple) -> list:
    """
    Renvoie la liste des points effectuant le plus court chemin entre
    un sommet de départ et sommet arrivée dansune matrice de coûts
    (déplacements: horizontaux, verticaux, diagonaux)
    avec l'algorithme de A*
    """
    matrice[arrivee] # Pour vérifier si l'arrivee est dans la matrice
    if(depart == arrivee): # le depart est il l'arrivee
        return [()]
    # Initialisation de la matrice de cout cummulee qui contient
    # la distance minimale pour aller a un sommet
    l, c = matrice.shape
    cout_cumul = np.matrix([[np.inf
            for y in range(c)] for x in range (l)])
    # tableau de precedence pour retrouver le chemin une fois
    # A* fini
    prec = np.array([[(-1,-1)
            for y in range(c)] for x in range (l)], dtype=object)
    # On initialise le couple pour le sommet de départ
    cout_cumul[depart[0],depart[1]] = float(0)
    chemin = []
    # Tas minimal
    tas = []
    # Pour savoir par où on est passé
    visite = set()
    # Pour initaliser l'algo
    courant = depart
    cout = 0

    n = l*c
    heappush(tas,(0,depart))
    # Tant que l'on ne trouve pas l'arrivée ou que le tas soit vide
    while courant != arrivee and tas != []:
        # On ajoute aux sommets visités le sommet courant
        if courant not in visite:
            visite.add(courant)
            # On détermine les voisins du sommet courant
            liste_voisin = voisin_dijkstra(matrice, *courant)
            # On parcours les voisins
            for voisin in liste_voisin:
                # On recupere les coordonnees et le cout du voisin
                voisin_cout, voisin_coords = voisin
                # On calcule le cout pour passer au voisin
                dis = sqrt(voisin_coords[0]**2+voisin_coords[1]**2)
                cout_suiv = voisin_cout + cout + distance_eucl(*courant, *voisin_coords)
                # Si le cout cumulé pour aller au voisin
                if(cout_cumul[voisin_coords] > cout_suiv):
                    heappush(tas, (cout_suiv, voisin_coords))
                    cout_cumul[voisin_coords] = cout_suiv
                    prec[voisin_coords] = courant
        # On recupere le prochain sommet avec un cout minimal
        cout, courant = heappop(tas)
    if tas == []:
        print("Pas de chemin")
        return [()]
    while(courant != depart):
        chemin.append(courant)
        courant = tuple(prec[courant])
    chemin.append(depart)
    chemin.reverse()
    return chemin

if __name__== "__main__":
    Matrice = np.matrix([[float('inf'), 3, float('inf'), 5, 8, 6, 7, 3, 3, float('inf')],
           [4, 5, 5, 5, 6, 6, 7, 3, 3, float('inf')],
           [5, 4, 4, 4, 6, 7, 8, 7, 3, float('inf')],
           [6, 5, 5, 4, 3, 6, 9, 8, 7, 7],
           [7, 7, 7, 6, 6, 6, 7, 8, 7, 7],
           [6, 7, 7, 7, 7, 5, 7, 4, 3, float('inf')],
           [8, 7, 8, 7, 7, 6, 6, float('inf'), float('inf'), float('inf')],
           [4, 5, 5, 8, 8, 6, 6, 6, 4, float('inf')],
           [3, 5, 5, 6, 6, 6, 6, 5, float('inf'), float('inf')],
           [float('inf'), 4, 4, 5, 5, 6, 6, float('inf'),float('inf'), float('inf')]])
    #Matrice = np.matrix([[1., 2.,5.,3.],[4., 2., 3., 9.,], [1., 7., 4., 5.,],[2., 6., 3., 8.,]])
    print(Matrice)    
    print(dijkstra(Matrice,(0,0),(9,9)))
    print(a_star(Matrice,(0,0),(9,1)))
    #print(voisin_dijkstra(Matrice, 0, 3))