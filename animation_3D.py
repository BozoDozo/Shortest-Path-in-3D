from OpenGL.GL import *  # exception car prefixe systematique
from OpenGL.GLU import *
from OpenGL.GLUT import *
from time import sleep
# todo direction
savex = 0
savey = 0


def animation(cpt_x, cpt_y, matrice_map):
    global savex, savey
    """
    ici on calcul la bonne translation a faire
    on n'a trouvé que cette facon de faire avec des if else
    """
    coord_x_open = cpt_x*2
    coord_y_open = cpt_y*2
    pente = 0
    pas = 0

    # savoir si on est dans un triangle
    if coord_y_open % 2 >= 1 and coord_x_open % 2 >= 1:
        # quelle partie du triangle
        if coord_y_open % 2 >= 1.5 and coord_x_open % 2 >= 1.5:
            if savey <= cpt_y:

                pente = matrice_map[int(cpt_x)+1, int(cpt_y)+1] -\
                    matrice_map[int(cpt_x+1), int(cpt_y)]
            else:
                pente = matrice_map[int(cpt_x+1), int(cpt_y)-1] - \
                    matrice_map[int(cpt_x+1), int(cpt_y)]
        else:
            if savey <= cpt_y:

                pente = matrice_map[int(cpt_x), int(cpt_y)+1] -\
                    matrice_map[int(cpt_x), int(cpt_y)]
            else:
                pente = matrice_map[int(cpt_x), int(cpt_y)-1] - \
                    matrice_map[int(cpt_x), int(cpt_y)]
    # pente y
    elif coord_y_open % 2 >= 1:
        if savey <= cpt_y:
            # comment avoir correctement la penst
            pente = matrice_map[int(cpt_x), int(cpt_y)+1] -\
                matrice_map[int(cpt_x), int(cpt_y)]
        else:
            pente = matrice_map[int(cpt_x), int(cpt_y)-1] - \
                matrice_map[int(cpt_x), int(cpt_y)]

        pas = (coord_y_open % 2 - 1)*pente
    # pente x
    elif coord_x_open % 2 >= 1:
        if savex <= cpt_x:

            pente = matrice_map[int(cpt_x)+1, int(cpt_y)] -\
                matrice_map[int(cpt_x), int(cpt_y)]
        else:
            pente = matrice_map[int(cpt_x)-1, int(cpt_y)] - \
                matrice_map[int(cpt_x), int(cpt_y)]

        pas = (coord_x_open % 2 - 1)*pente

    savex = cpt_x
    savey = cpt_y

    glTranslated(0+coord_y_open, 0+coord_x_open,
                 matrice_map[int(cpt_x), int(cpt_y)]+0.5+pas)
    glMaterialfv(GL_FRONT_AND_BACK,
                 GL_AMBIENT_AND_DIFFUSE, [0, 0, 1,     1.0])
    glutSolidSphere(0.5, 5, 5)
