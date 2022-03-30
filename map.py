#mes biblio
from OpenGL.GL import *  # exception car prefixe systematique
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import sin, cos
import sys
from random import *

def generation_matrice(n):
    #generation& d'une liste nxn avec nombre alea*
    #nombre de 1 a 10
    map=[]

    for i in range(n):
        ligne=[]
        for j in range(n):
            nb=randint(1,10)
            ligne.append(nb)

        map.append(ligne)
    return map
#------------------------------------------
def median(matrice,j,i):
    nb=[]
    cpth=0
    cptb=0
    n=len(matrice)
    #poly ou on est
    nb.append(matrice[j][i])
    if i-1>=0:

        #poly de gauche
        nb.append(matrice[j][i-1])
        if j-1>=0:

            #diago et en bas
            nb.append(matrice[j-1][i-1])
            nb.append(matrice[j-1][i])
            cptb=1
        if j+1<n:

            #diago et en haut*
            nb.append(matrice[j+1][i-1])
            nb.append(matrice[j+1][i])
            cpth=1
    if i+1<n:
        #poly de droit

        nb.append(matrice[j][i+1])
        if j-1>=0:

            #diago et en bas
            nb.append(matrice[j-1][i+1])

            if cptb==0:
                nb.append(matrice[j-1][i])
        if j+1<n:

            #diago et en haut
            nb.append(matrice[j+1][i+1])
            if cpth==0:
                nb.append(matrice[j+1][i])
    nb.sort()
    if len(nb)%2==0:
        nombre=nb[len(nb)//2]
    else:
        nombre=nb[(len(nb)//2)+1]
    return nombre

def tukey(matrice):
    n=len(matrice)
    matrice_b=[]


    for j in range(n):
        ligne=[]
        for i in range(n):
            nb=median(matrice,j,i)

            ligne.append(nb)
        matrice_b.append(ligne)
    print(matrice,"\n\n",matrice_b)
    return matrice_b
#--------------------------------------




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
