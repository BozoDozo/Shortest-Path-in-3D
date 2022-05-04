from random import *
from typing import List

def generation_matrice_carre_aleatoire(n: int, borne_inf: int = 1,
                                       borne_sup: int = 10) -> List[List[int]]:
    """
    Genère une matrice de valeurs entre 2 bornes
    """
    return [[randint(borne_inf, borne_sup)
                for x in range(n)] for y in range (n)]

def generation_matrice_carre(n: int):
    """generation& d'une matrice nxn avec des nombres alea*
    nombre de 1 a 10
    """
    map=[]

    nb=1
    for i in range(n):
        ligne=[]
        for j in range(n):
            ligne.append(nb)
            nb=nb+1

        map.append(ligne)

    return map

def faire_couleur(nbr):
    """
    calcul d"une couleur aleatoire  par rapport au  cout
    """
    #70 et juste un facteur
    nbr=999-(nbr*70)
    if nbr<100:
        nbr=nbr*5
        nbr_couleur="#000"+str(int(nbr))+"000"
    else:
        nbr_couleur="#000"+str(int(nbr))+"000"
    return nbr_couleur

def creation_map(liste_square_map_id,canva,liste_cout,n):
    """
     dans cette fonction nous créons la map en recuperant les identifiant
    """

    width_square=50
    xa=0
    ya=0
    xb=width_square
    yb=width_square
    for j in range(0,n):
        ligne=[]
        for i in range(0,n):
            couleur=faire_couleur(liste_cout[j][i])
            id=canva.create_rectangle(xa,ya,xb,yb,fill=couleur)
            ligne.append(id)
            xa=xa+width_square
            xb=xb+width_square
        liste_square_map_id.append(ligne)
        ya=ya+width_square
        yb=yb+width_square
        xa=0
        xb=width_square
    return liste_square_map_id

def mettre_couleur_dep_ar(liste_square_map_id,depart,arrive,canva,n):
    #pour avoir les coord dans le tableau
    xd=depart//n
    yd=depart%n
    xa=arrive//n
    ya=arrive%n

    canva.itemconfigure(liste_square_map_id[xa][ya],fill="red")
    canva.itemconfigure(liste_square_map_id[xd][yd],fill="yellow")
