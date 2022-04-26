from random import *

def generation_matrice(n):
    """generation& d'une matrice nxn avec des nombres alea*
    nombre de 1 a 10"""
    map=[]

    for i in range(n):
        ligne=[]
        for j in range(n):
            nb=randint(1,10)

            ligne.append(nb)

        map.append(ligne)

    return map

def generation_matrice_carre(n):
    """generation& d'une matrice nxn avec des nombres alea*
    nombre de 1 a 10"""
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
    print(nbr)
    coul=10*nbr
    if nbr>=8:
        nbr_couleur="#FFF"
    elif coul<100:
        nbr_couleur="#"+str(coul)+"0"

    else:
        nbr_couleur="#"+str(coul)

    return nbr_couleur
def creation_map(liste_square_map_id,canva,liste_cout,n):
    """
     dans cette fonction nous créons la map en recuperant les identifiant
    """
    #coordonné pour les carré
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

    xd=depart//n
    yd=depart%n
    xa=arrive//n
    ya=arrive%n

    canva.itemconfigure(liste_square_map_id[xa][ya],fill="red")
    canva.itemconfigure(liste_square_map_id[xd][yd],fill="yellow")
