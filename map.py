#mes biblio
from OpenGL.GL import *  # exception car prefixe systematique
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import sin, cos
import sys
from random import randint
from typing import List, Union

def min_matrix(matrice: List[List[int]]) -> Union[int, float]:
    """
    Retourne la valeur minimale d'une matrice
    """
    val_min = float("inf")
    for ligne in matrice:
        min_cour = max(ligne)
        if(min_cour < val_min):
            val_min = min_cour
    return val_min


def generation_matrice_carre_aleatoire(n: int, borne_inf: int = 1,
                                       borne_sup: int = 10) -> List[List[int]]:
    """
    Genère une matrice de valeurs entre 2 bornes
    """
    return [[randint(borne_inf, borne_sup)
                for x in range(n)] for y in range (n)]

def ajout_obstacle(matrice: List[List[int]]):
    """
    Créer des obstacles dans la valeur minimale de la matrice de coût
    """
    min_val = min_matrix(matrice)
    for i in range(len(matrice)):
        for j in range(len(matrice[0])):
            if(matrice[i][j] == min_val):
                matrice[i][j] = float("inf")


def clipping_voisin(matrice: List[List[int]], i: int, j: int,
                                                 rayon : int = 1) -> List[int]:
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


def tukey(matrice: List[List[int]], rayon : int = 1) -> List[List[int]]:
    """
    Renvoie une matrice bruite avec le bruit de tukey
    possibilite de mettre un rayon
    """
    n = len(matrice)

    #Initialisaton d'un matrice receptrice
    mat_median = [[0 for x in range(n)] for y in range (n)]


    for i in range(n):
        for j in range(n):
            mat_median[i][j] = median(clipping_voisin(matrice, i, j, rayon))


    return mat_median



def median(vec: List[int]) -> int:
    """
    Renvoie la valeur médiane d'une liste de données
    """
    n = len(vec)
    vec.sort()

    #Verification de la parité
    if n&1:
        return vec[n//2]

    else:
        return ((vec[n//2-1] + vec[n//2]) // 2)

def generation_matrice_terrain(n: int, borne_inf: int = 1, borne_sup: int = 10,
                     rayon : int = 1, obstacle: bool = False)-> List[List[int]]:
    """
    Génération de matrice pour le terrain
    """
    matrice = tukey(generation_matrice_carre_aleatoire(n, borne_inf, borne_sup),
                                                                         rayon)
    if obstacle:
        ajout_obstacle(matrice)

    return matrice

def gestion_poly(matrice):
    #faire les poly separer
    #recuperation de la longeur
    n=len(matrice)

    #pour avoir ecart en x y

    ecarty=0

    for i in range(n):
        ecartx=0
        if i>=1:
            ecarty=2
        for j in range(n):
            if j>=1:
                ecartx=2
            col=matrice[j][i]
            glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [col*0.1, col*0.1, col*0.1, 1.0])
            glBegin(GL_POLYGON);

            glVertex3f(j*ecartx, i*ecarty, matrice[i][j]);
            glVertex3f(j*ecartx, i*ecarty+1, matrice[i][j]);

            glVertex3f(j*ecartx, i*ecarty+1, matrice[i][j]);
            glVertex3f(j*ecartx+1, i*ecarty+1, matrice[i][j]);

            glVertex3f(j*ecartx+1, i*ecarty+1, matrice[i][j]);
            glVertex3f(j*ecartx+1, i*ecarty, matrice[i][j]);

            glVertex3f(j*ecartx+1, i*ecarty, matrice[i][j]);
            glVertex3f(j*ecartx, i*ecarty, matrice[i][j]);
            glEnd()

def gestion_poly_trx(matrice):
        #faire les poly separer
        #recuperation de la longeur
        n=len(matrice)

        #pour avoir ecart en x y

        ecarty=0

        for i in range(n):
            ecartx=0
            if i>=1:
                ecarty=2
                if i==n:
                    break
            for j in range(n):

                if j>=1:
                    ecartx=2
                if j==n-1:
                    break

                col=matrice[j][i]
                glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0, 0, 1, 1.0])
                glBegin(GL_POLYGON);
                #00 01
                glVertex3f(j*ecartx+1, i*ecarty, matrice[i][j]);
                glVertex3f(j*ecartx+1, i*ecarty+1, matrice[i][j]);

                glVertex3f(j*ecartx+1, i*ecarty+1, matrice[i][j]);
                glVertex3f(j*ecartx+2, i*ecarty+1, matrice[i][j+1]);

                glVertex3f(j*ecartx+2, i*ecarty+1, matrice[i][j+1]);
                glVertex3f(j*ecartx+2, i*ecarty, matrice[i][j+1]);

                glVertex3f(j*ecartx+2, i*ecarty, matrice[i][j+1]);
                glVertex3f(j*ecartx+1, i*ecarty, matrice[i][j]);
                glEnd()

def gestion_poly_try(matrice):
        #faire les poly separer
        #recuperation de la longeur
        n=len(matrice)
        #pour avoir ecart en x y
        ecarty=0

        for i in range(n):
            ecartx=0
            if i>=1:
                ecarty=2
                if i==n-1:
                    break
            for j in range(n):
                if j>=1:
                    ecartx=2
                if j==n:
                    break

                col=matrice[j][i]
                glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [1, 0, 0, 1.0])
                glBegin(GL_POLYGON);
                #00 01
                glVertex3f(j*ecartx, i*ecarty+1, matrice[i][j]);
                glVertex3f(j*ecartx, i*ecarty+2, matrice[i+1][j]);

                glVertex3f(j*ecartx, i*ecarty+2, matrice[i+1][j]);
                glVertex3f(j*ecartx+1, i*ecarty+2, matrice[i+1][j]);

                glVertex3f(j*ecartx+1, i*ecarty+2, matrice[i+1][j]);
                glVertex3f(j*ecartx+1, i*ecarty+1, matrice[i][j]);

                glVertex3f(j*ecartx+1, i*ecarty+1, matrice[i][j]);
                glVertex3f(j*ecartx, i*ecarty+1, matrice[i][j]);
                glEnd()

def gestion_poly_tr_trigd(matrice):
        #faire les poly separer
        #recuperation de la longeur
        n=len(matrice)
        #pour avoir ecart en x y
        ecarty=0

        for i in range(n):
            ecartx=0
            if i>=1:
                ecarty=2
                if i==n-1:
                    break
            for j in range(n):
                if j>=1:
                    ecartx=2
                if j==n-1:
                    break

                col=matrice[j][i]
                glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [1, 1, 0, 1.0])
                glBegin(GL_POLYGON);
                #00 01
                glVertex3f(j*ecartx+1, i*ecarty+1, matrice[i][j]);
                glVertex3f(j*ecartx+1, i*ecarty+2, matrice[i+1][j]);

                glVertex3f(j*ecartx+1, i*ecarty+2, matrice[i+1][j]);
                glVertex3f(j*ecartx+2, i*ecarty+1, matrice[i][j+1]);

                glVertex3f(j*ecartx+2, i*ecarty+1, matrice[i][j+1]);
                glVertex3f(j*ecartx+1, i*ecarty+1, matrice[i][j]);

                glEnd()
                glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0, 1, 1, 1.0])
                glBegin(GL_POLYGON);
                #00 01
                glVertex3f(j*ecartx+2, i*ecarty+2, matrice[i+1][j+1]);
                glVertex3f(j*ecartx+1, i*ecarty+2, matrice[i+1][j]);

                glVertex3f(j*ecartx+1, i*ecarty+2, matrice[i+1][j]);
                glVertex3f(j*ecartx+2, i*ecarty+1, matrice[i][j+1]);

                glVertex3f(j*ecartx+2, i*ecarty+1, matrice[i][j+1]);
                glVertex3f(j*ecartx+2, i*ecarty+2, matrice[i+1][j+1]);

                glEnd()

def grid_map(matrice_map):
    #generation poly separe
    gestion_poly(matrice_map)
    #generation poly transi
    gestion_poly_trx(matrice_map)
    gestion_poly_try(matrice_map)
    gestion_poly_tr_trigd(matrice_map)

if __name__ == "__main__":

    mat = generation_matrice_terrain(5, obstacle=True)
    print(mat)
    print(min_matrix(mat))
