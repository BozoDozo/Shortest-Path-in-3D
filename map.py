# mes biblio
from OpenGL.GL import *  # exception car prefixe systematique
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import sin, cos
import sys
from random import *
from dijkstra import *
from bezier import *


def generation_matrice(n):
    """generation& d'une matrice nxn avec des nombres alea*
    nombre de 1 a 10"""
    map = []

    for i in range(n):
        ligne = []
        for j in range(n):
            nb = randint(1, 10)
            ligne.append(nb)

        map.append(ligne)
    """ map sujet projet"""
    # map=[[0,5,11,13,16,5,4,19,10,18],[16,1,6,17,2,7,1,15,16,4],[4,8,23,23,11,8,4,16,11,1],[1,13,3,17,11,9,14,8,3,5],[3,16,11,13,1,3,12,14,12,13],[1,3,5,16,7,6,15,15,14,3],[12,18,4,15,16,8,16,17,4,1],[12,5,15,10,9,19,18,7,4,7],[17,3,14,16,5,14,3,19,4,19],[2,11,18,10,19,2,19,13,19,0]]

    return map


""" --------------------------moyyennage---------------------------------"""


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
    for k in range(diag_haut_x, diag_bas_x+1):
        for l in range(diag_bas_y, diag_haut_y+1):
            vec.append(matrice[k][l])

    return vec


def tukey(matrice, rayon=1):
    """
    Renvoie une matrice bruite avec le bruit de tukey
    possibilite de mettre un rayon
    """
    n = len(matrice)

    # Initialisaton d'un matrice receptrice
    mat_median = [[0 for x in range(n)] for y in range(n)]

    for i in range(n):
        for j in range(n):
            mat_median[i][j] = median(clipping_voisin(matrice, i, j, rayon))

    return mat_median


def median(vec):
    """
    Renvoie la valeur médiane d'une liste de données
    """
    n = len(vec)
    vec.sort()

    # Verification de la parité
    if n & 1:
        return vec[n//2]

    else:
        return ((vec[n//2-1] + vec[n//2]) // 2)


"""-------------------creation de poly ------------------"""


def hex_to_rgb(value: str):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_hex(red: int, green: int, blue: int):
    """Return color as #rrggbb for the given color values."""
    return '#%02x%02x%02x' % (red, green, blue)


def normalisation(valeur) -> float:
    """
    Normalise d'une valeur en fonction du minimum et du maximum
    """
    return (valeur-1)/9


def shade_color(color, factor: int):
    """
    Retourne la couleur rgb assombri ou éclaircir
    """
    shaded_color = []
    for c in color:
        x = int(c * factor)
        if(x > 255):
            x = 255
        if(x < 0):
            x = 0
        shaded_color.append(x)
    return shaded_color


def get_color(val) -> str:
    """
    Récupère la couleur en niveau de gris
    pour une intensité donnée
    """
    if(val == float('inf')):
        color = (0, 0, 0)
    else:
        norm = normalisation(val)
        norm = round(norm, 1)
        color = (norm, norm, norm, 1)
    print(color)
    return color


def gestion_poly(matrice):
    # faire les poly separer
    # recuperation de la longeur
    n = len(matrice)

    # pour avoir ecart en x y

    ecarty = 0

    for i in range(n):
        ecartx = 0
        if i >= 1:
            ecarty = 2
        for j in range(n):
            if j >= 1:
                ecartx = 2
            col = get_color(matrice[i][j])

            glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
                         col)
            glBegin(GL_POLYGON)

            glVertex3f(j*ecartx, i*ecarty, matrice[i][j])
            glVertex3f(j*ecartx, i*ecarty+1, matrice[i][j])

            glVertex3f(j*ecartx, i*ecarty+1, matrice[i][j])
            glVertex3f(j*ecartx+1, i*ecarty+1, matrice[i][j])

            glVertex3f(j*ecartx+1, i*ecarty+1, matrice[i][j])
            glVertex3f(j*ecartx+1, i*ecarty, matrice[i][j])

            glVertex3f(j*ecartx+1, i*ecarty, matrice[i][j])
            glVertex3f(j*ecartx, i*ecarty, matrice[i][j])
            glEnd()


def gestion_poly_trx(matrice):
    # faire les poly separer
    # recuperation de la longeur
    n = len(matrice)

    # pour avoir ecart en x y

    ecarty = 0

    for i in range(n):
        ecartx = 0
        if i >= 1:
            ecarty = 2
            if i == n:
                break
        for j in range(n):
            if j >= 1:
                ecartx = 2
            if j == n-1:
                break

            col = matrice[j][i]
            glMaterialfv(GL_FRONT_AND_BACK,
                         GL_AMBIENT_AND_DIFFUSE, [0, 0.5, 0, 1.0])
            glBegin(GL_POLYGON)
            # 00 01
            glVertex3f(j*ecartx+1, i*ecarty, matrice[i][j])
            glVertex3f(j*ecartx+1, i*ecarty+1, matrice[i][j])

            glVertex3f(j*ecartx+1, i*ecarty+1, matrice[i][j])
            glVertex3f(j*ecartx+2, i*ecarty+1, matrice[i][j+1])

            glVertex3f(j*ecartx+2, i*ecarty+1, matrice[i][j+1])
            glVertex3f(j*ecartx+2, i*ecarty, matrice[i][j+1])

            glVertex3f(j*ecartx+2, i*ecarty, matrice[i][j+1])
            glVertex3f(j*ecartx+1, i*ecarty, matrice[i][j])
            glEnd()


def gestion_poly_try(matrice):
    # faire les poly separer
    # recuperation de la longeur
    n = len(matrice)
    # pour avoir ecart en x y
    ecarty = 0

    for i in range(n):
        ecartx = 0
        if i >= 1:
            ecarty = 2
            if i == n-1:
                break
        for j in range(n):
            if j >= 1:
                ecartx = 2
            if j == n:
                break

            col = matrice[j][i]
            glMaterialfv(GL_FRONT_AND_BACK,
                         GL_AMBIENT_AND_DIFFUSE, [0, 0.5, 0, 1.0])
            glBegin(GL_POLYGON)
            # 00 01
            glVertex3f(j*ecartx, i*ecarty+1, matrice[i][j])
            glVertex3f(j*ecartx, i*ecarty+2, matrice[i+1][j])

            glVertex3f(j*ecartx, i*ecarty+2, matrice[i+1][j])
            glVertex3f(j*ecartx+1, i*ecarty+2, matrice[i+1][j])

            glVertex3f(j*ecartx+1, i*ecarty+2, matrice[i+1][j])
            glVertex3f(j*ecartx+1, i*ecarty+1, matrice[i][j])

            glVertex3f(j*ecartx+1, i*ecarty+1, matrice[i][j])
            glVertex3f(j*ecartx, i*ecarty+1, matrice[i][j])
            glEnd()


def gestion_poly_tr_trigd(matrice):
    # faire les poly separer
    # recuperation de la longeur
    n = len(matrice)
    # pour avoir ecart en x y
    ecarty = 0

    for i in range(n):
        ecartx = 0
        if i >= 1:
            ecarty = 2
            if i == n-1:
                break
        for j in range(n):
            if j >= 1:
                ecartx = 2
            if j == n-1:
                break

            col = matrice[j][i]
            glMaterialfv(GL_FRONT_AND_BACK,
                         GL_AMBIENT_AND_DIFFUSE, [0, 1, 1, 1.0])
            glBegin(GL_POLYGON)
            # 00 01
            glVertex3f(j*ecartx+1, i*ecarty+1, matrice[i][j])
            glVertex3f(j*ecartx+1, i*ecarty+2, matrice[i+1][j])

            glVertex3f(j*ecartx+1, i*ecarty+2, matrice[i+1][j])
            glVertex3f(j*ecartx+2, i*ecarty+1, matrice[i][j+1])

            glVertex3f(j*ecartx+2, i*ecarty+1, matrice[i][j+1])
            glVertex3f(j*ecartx+1, i*ecarty+1, matrice[i][j])

            glEnd()
            glMaterialfv(GL_FRONT_AND_BACK,
                         GL_AMBIENT_AND_DIFFUSE, [0, 1, 1, 1.0])
            glBegin(GL_POLYGON)
            # 00 01
            glVertex3f(j*ecartx+2, i*ecarty+2, matrice[i+1][j+1])
            glVertex3f(j*ecartx+1, i*ecarty+2, matrice[i+1][j])

            glVertex3f(j*ecartx+1, i*ecarty+2, matrice[i+1][j])
            glVertex3f(j*ecartx+2, i*ecarty+1, matrice[i][j+1])

            glVertex3f(j*ecartx+2, i*ecarty+1, matrice[i][j+1])
            glVertex3f(j*ecartx+2, i*ecarty+2, matrice[i+1][j+1])

            glEnd()


def tracer_dijkstra(liste, matrice):
    cpt = 0
    n = len(matrice)
    while cpt < len(liste)-2:
        # point de depart segment
        i_a = liste[cpt]//n
        j_a = liste[cpt] % n
        z_a = matrice[i_a][j_a]
        # point arrive segment
        i_b = liste[cpt]//n
        j_b = liste[cpt] % n
        z_b = matrice[i_a][j_a]

        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0, 1, 1, 1])
        glBegin(GL_POLYGON)
        glVertex3f(j_a, i_a, 0)
        glVertex3f(j_a, i_a+1, 0)

        glVertex3f(j_a, i_a+1, 0)
        glVertex3f(j_b, i_b+1, 0)

        glVertex3f(j_b, i_b+1, 0)
        glVertex3f(j_b, i_b, 0)

        glVertex3f(j_b, i_b, 0)
        glVertex3f(j_a, i_a, 0)

        glEnd()
        # pour passe au prochain segment
        cpt = cpt+1


def gestion_poly_map():
    for i in range(50):
        for j in range(50):
            glMaterialfv(GL_FRONT_AND_BACK,
                         GL_AMBIENT_AND_DIFFUSE, [1, 0, 0, 1.0])
            glBegin(GL_POLYGON)

            glVertex3f(j, i, 0)
            glVertex3f(j, i+1, 0)

            glVertex3f(j, i+1, 0)
            glVertex3f(j+1, i+1, 0)

            glVertex3f(j+1, i+1, 0)
            glVertex3f(j+1, i, 0)

            glVertex3f(j+1, i, 0)
            glVertex3f(j, i, 0)
            glEnd()


def liste_coor_djikstra(liste):
    liste_coord = []
    for i in range(len(liste)):

        x = liste[i]//10
        y = liste[i] % 10
        liste_coord.append((x, y))

    return liste_coord


def grid_map(matrice_map):
    """generation poly separe"""
    gestion_poly(matrice_map)
    """generation poly transi"""
    gestion_poly_trx(matrice_map)
    gestion_poly_try(matrice_map)
    gestion_poly_tr_trigd(matrice_map)
    # glTranslated(-12,-12,0)
    # gestion_poly_map()
    """TRACER dijkstra"""
    liste = djikstra(matrice_map, 0, 85)
    liste_coors_dji = liste_coor_djikstra(liste)

    it = 100

    trace_beizier(liste_coors_dji, it)
    voir_bezier(liste_point_bezier)
    # tracer_dijkstra(liste,matrice_map)

    # liste=djikstra(matrice_map,0,99)
    # tracer_dijkstra(liste,matrice_map)
