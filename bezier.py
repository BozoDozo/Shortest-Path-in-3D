import tkinter as tk
from chenille_2D import Chenille_2D
from time import sleep
mobile_2D = None
Canva = None
cote = None
def bary_bezier(x0,y0,x1,y1,x2,y2,x3,y3,t):
    """
    Calcule les barycentres des 4 points de controles
    avec un coefficient t
    """
    #Generation 1
    x0i = (1 - t) * x0 + x1 * t
    y0i = (1 - t) * y0 + y1 * t
    x1i = (1 - t) * x1 + x2 * t
    y1i = (1 - t) * y1 + y2 * t
    x2i = (1 - t) * x2 + x3 * t
    y2i = (1 - t) * y2 + y3 * t

    x0, y0, x1, y1,x2, y2 = x0i,y0i,x1i,y1i,x2i,y2i

    #Generation 2
    x0i = (1 - t) * x0 + x1 * t
    y0i = (1 - t) * y0 + y1 * t
    x1i = (1 - t) * x1 + x2 * t
    y1i = (1 - t) * y1 + y2 * t

    x0, y0, x1, y1 = x0i,y0i,x1i,y1i

    #Generation 3
    x0i = (1 - t) * x0 + x1 * t
    y0i = (1 - t) * y0 + y1 * t

    return x0i,y0i

def get_info(canvas: tk.Canvas, taille_carres: int):
    global Canva, cote
    Canva = canvas
    cote = taille_carres

def trace_beizier_quatre(x0, y0, x1, y1, x2, y2, x3, y3, it, debut=0):
    """
    Calcule les barycentres de 4 points avec un nombre d'itérations
    la variable debut definit l'endroit où la courbe commence s'afficher
     exemple 0.25 on commence au 2ème point de controle
    """
    u = debut
    pas = 1/it
    #xi, yi = bary_bezier(x0,y0,x1,y1,x2,y2,x3,y3,u)
    while (u <= 1):
        xi, yi = bary_bezier(x0,y0,x1,y1,x2,y2,x3,y3,u)
        mobile_2D.deplacement(xi, yi)
        Canva.update()
        sleep(0.01)
        u += pas

def trace_beizier(liste_points:list, it: int, _2D: Chenille_2D):
    """
    Trace une coube de bézier sur OpenGL, prend en paramètre
    une liste de points
    """
    global mobile_2D
    n = len(liste_points)
    if(n < 4):
        print("Pas assez de points")
        return -1
    mobile_2D = _2D
    #mobile_2D = Chenille_2D(*liste_points[0], 7, Canva, cote)
    n_hors  = (n - 4)%3 # n_hors donne le nombre de points qui ne sont
                        # pas dans un quadruplet

    n_int = n-n_hors-1
    # On trace la courbe pour le cas général
    # for i in range(0, n_int, 3):
    i = 0
    while( i < n_int):
        trace_beizier_quatre(*liste_points[i],*liste_points[i+1],
                                    *liste_points[i+2], *liste_points[i+3],it)
        i+=3

    # On vérifie que l'on ne se trouve pas dans le cas particulier où
    # il n'y que 4 points dans la liste
    if(n != 4):

        # Il y a 2 points hors des quadruplets
        if n_hors == 2:
            trace_beizier_quatre(*liste_points[-4],*liste_points[-3],
                                        *liste_points[-2], *liste_points[-1],
                                                                      it, 0.25)

        # Il y a 1 point hors des quadruplets
        elif n_hors == 1:
            trace_beizier_quatre(*liste_points[-4],*liste_points[-3],
                                        *liste_points[-2], *liste_points[-1],
                                                                       it, 0.75)
        # Trace sur OpenGL le dernier point de la courbe
        mobile_2D.deplacement(*liste_points[-1])
      
    mobile_2D.delete()