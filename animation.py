from OpenGL.GL import *  # exception car prefixe systematique
from OpenGL.GLU import *
from OpenGL.GLUT import *

def animation(cpt_x,cpt_y,matrice_map):


    x=cpt_x/2
    y=cpt_y/2
    pente=0
    if (cpt_x%2)>=1 and (cpt_y%2)<=1:
        if (cpt_x%2)>=(cpt_y%2):
            pente=matrice_map[int(y)][int(x)+1]-matrice_map[int(y)][int(x)]
            pente=((cpt_x%2)-1)*pente
        else:
            pente=matrice_map[int(y)+1][int(x)]-matrice_map[int(y)][int(x)]
            pente=((cpt_x%2)-1)*pente
    if (cpt_x%2)>=1:
        pente=matrice_map[int(y)][int(x)+1]-matrice_map[int(y)][int(x)]
        pente=((cpt_x%2)-1)*pente
    if (cpt_y%2)>=1:
        pente=matrice_map[int(y)+1][int(x)]-matrice_map[int(y)][int(x)]
        pente=((cpt_y%2)-1)*pente

    glTranslated(0+cpt_x,0+cpt_y,matrice_map[int(y)][int(x)]+0.5+pente)
    glutSolidSphere(0.5,5,5)
    glTranslated(-0.5,0,0)
    glutSolidSphere(0.4,5,10)
