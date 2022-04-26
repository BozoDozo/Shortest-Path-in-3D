
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


def trace_beizier_quatre(x0, y0, x1, y1, x2, y2, x3, y3, it, debut=0):
    """
    Calcule les barycentres de 4 points avec un nombre d'itérations
    la variable debut definit l'endroit où la courbe commence s'afficher
     exemple 0.25 on commence au 2ème point de controle
    """
    global canva
    pas=1/it
    u = debut
    while(u < 1):
        xi, yi = bary_bezier(x0,y0,x1,y1,x2,y2,x3,y3,u)
        #Tracer OpenGL le point xi, yi
        canva.create_line(xi,yi,xi+1,yi+1)
        u += pas




def trace_beizier(liste_points,it):
    """
    Trace une courbe de bézier sur OpenGL, prend en paramètre
    une liste de points
    """
    liste_points=liste_points[:-1]
    n = len(liste_points)

    if(n < 4):
        print("Pas assez de points")
        return -1

    n_hors  = (n - 4)%3 #n_hors donne le nombre de points qui ne sont
                        # pas dans un quadruplet

    n_int = n-n_hors
    #On trace la courbe pour le cas général
    for i in range(0, n_int, 3):
        trace_beizier_quatre(*liste_points[i],*liste_points[i+1],
                                    *liste_points[i+2], *liste_points[i+3],it)

    #On vérifie que l'on ne se trouve pas dans le cas particulier où
    # il n'y que 4 points dans la liste
    if(n != 4):

        #Il y a 2 points hors des quadruplets
        if n_hors == 2:
            trace_beizier_quatre(*liste_points[-4],*liste_points[-3],
                                        *liste_points[-2], *liste_points[-1],
                                                                      it, 0.25)

        #Il y a 1 point hors des quadruplets
        elif n_hors == 1:
            trace_beizier_quatre(*liste_points[-4],*liste_points[-3],
                                        *liste_points[-2], *liste_points[-1],
                                                                       it, 0.75)
        #Trace sur OpenGL le dernier point de la courbe
