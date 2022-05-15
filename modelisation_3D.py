#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

###############################################################
from OpenGL.GL import *  # exception car prefixe systematique
from OpenGL.GLU import *
from OpenGL.GLUT import *
from map import grid_map
from animation_3D import animation

from time import sleep
###############################################################

# Variables Globales
cpt = 0
cpt_x = 0
cpt_y = 0
# cpt pour translate
cpt_translate = 0
# postitionement
x_pos, y_pos, z_pos = 0, 0, 0

eye_angle_x, eye_angle_y, eye_angle_z = 315, 50, 210
eye = [0, 0, 50]
center = [10, 0, 10]
up_vec = [1, 1, 0]

# Couleurs
diffuse = [0.7, 0.7, 0.7, 1.0]
specular = [0.001, 0.001, 0.001, 1.0]
pos = [1, 1, -1, 0]

anim = False
anim_bouton = False
quadric = None
DISPLAY_GRID = False
rotate_x = 30
rotate_y = 15
translate_z = 4
# normals
normal = []
normals = 0
chemin = []
# depart arriver
depart_open = None
arrivee_open = None
############################################################## #
n = 10
matrice_map = []
trajet_open = []


def init():
    global quadric, pos
    # clear color to black
    glClearColor(0.0, 0.0, 0.0, 0.0)

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    glEnable(GL_LIGHT0)

    glLightfv(GL_LIGHT0, GL_POSITION, pos)

    glEnable(GL_LIGHTING)
    glShadeModel(GL_FLAT)

    quadric = gluNewQuadric()

    gluQuadricDrawStyle(quadric, GLU_FILL)


def display():
    global cpt_x, cpt_y, cpt_z, cpt, anim, anim_bouton
    global eye_angle_x, eye_angle_y, eye_angle_z, center, up_vec
    global trajet_open
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glPushMatrix()

    # Modelisation du repere othonorme
    # centre
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [1, 1, 1, 1.0])
    gluSphere(quadric, 0.2, 20, 16)

    # Axe z Bleu
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0, 0, 1, 1.0])
    gluCylinder(quadric, 0.1, 0.1, 1000, 20, 16)

    # Axe y Vert
    glPushMatrix()
    glRotatef(90, 0, 1, 0)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0, 1, 0, 1.0])
    gluCylinder(quadric, 0.1, 0.1, 1000, 20, 16)
    glPopMatrix()

    # Axe x Rouge
    glPushMatrix()
    glRotatef(-90, 1, 0, 0)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [1, 0, 0, 1.0])
    gluCylinder(quadric, 0.1, 0.1, 1000, 20, 16)
    glPopMatrix()

    # creation de la map
    grid_map(matrice_map)
    # creation normals pour les polygon plat
    if normals != 0:
        for j in range(0, n):
            ligne = []
            for i in range(0, n):
                print("toto", i)
                if (j % 2) >= 1 and (i % 2) >= 1:

                    ligne.append((j, i, matrice_map[i, j]))
                # pente x
                elif (i % 2) >= 1:
                    ligne.append((j, i, matrice_map[i, j]))

                    # penty
                elif (j % 2) >= 1:

                    ligne.append((j, i, matrice_map[i, j]))

                else:
                    ligne.append((j, i, matrice_map[i, j]))
            normal.append(ligne)
        #########################################
        # création des normes et affichage
        glMaterialfv(GL_FRONT_AND_BACK,
                     GL_AMBIENT_AND_DIFFUSE, [1, 0, 0, 1.0])
        glBegin(GL_LINES)
        for j in range(10):

            for i in range(10):
                # poly plat

                glVertex3f(normal[j][i][0]*2+0.5, normal[j]
                           [i][1]*2+0.5, normal[j][i][2])
                glVertex3f(normal[j][i][0]*2+0.5, normal[j]
                           [i][1]*2+0.5, normal[j][i][2]+3)
                if j != 9 and i != 9:
                    # POLY PENTE y
                    pente_x = matrice_map[j, i+1]-matrice_map[j, i]
                    point_x = matrice_map[j, i]+(pente_x/2)
                    # point millieuxx
                    point_tx = (i*2+1+i*2+2+i*2+1)/3
                    point_ty = (j*2+1+j*2+1+j*2+2)/3
                    point_tz = (matrice_map[j, i+1]+matrice_map[j, i] +
                                matrice_map[j+1, i])/3
                    # produit vec pour triangle  gauche
                    vec_a = [1, 0, matrice_map[j, i+1]-matrice_map[j, i]]
                    vec_b = [0, 1, matrice_map[j+1, i]-matrice_map[j, i]]
                    a = vec_a[1]*vec_b[2]-vec_a[2]*vec_b[1]
                    b = -vec_a[0]*vec_b[2]-vec_a[2]*vec_b[0]
                    c = vec_a[0]*vec_b[1]-vec_a[1]*vec_b[0]
                    vec_c = [a, b, c]

                    glVertex3f(point_tx, point_ty, point_tz)
                    glVertex3f(point_tx+vec_c[0], point_ty+vec_c[1],
                               point_tz+vec_c[2])

                    if i >= 1:
                        point_tx = (i*2+i*2+i*2-1)/3
                        point_ty = (j*2+2+j*2+1+j*2+1)/3

                        point_tz = (matrice_map[j+1, i]+matrice_map[j, i] +
                                    matrice_map[j+1, i-1])/3

                        vec_a = [0, 1, matrice_map[j+1, i]-matrice_map[j, i]]
                        vec_b = [-1, -1, matrice_map[j+1, i-1]-matrice_map[j, i]]

                        a = vec_a[1]*vec_b[2]-vec_a[2]*vec_b[1]
                        b = -vec_a[0]*vec_b[2]-vec_a[2]*vec_b[0]
                        c = vec_a[0]*vec_b[1]-vec_a[1]*vec_b[0]
                        vec_c = [a, b, c]

                        glVertex3f(point_tx, point_ty, point_tz)
                        glVertex3f(point_tx+vec_c[0], point_ty+vec_c[1],
                                   point_tz+vec_c[2])
                    if point_x == matrice_map[j, i]:
                        # if c'est plat
                        glVertex3f(normal[j][i][1]*2+1.5,
                                   normal[j][i][0]*2+0.5, point_x)
                        glVertex3f(normal[j][i][1]*2+1.5,
                                   normal[j][i][0]*2+0.5,  point_x+3)

                    else:
                        # pente qui augmente
                        pente_xbis = -1/pente_x

                        if pente_x < 0:
                            # x,y,z
                            # pente_x
                            point_xbis = point_x+pente_xbis

                            glVertex3f(normal[j][i][1]*2+1.5, normal[j]
                                       [i][0]*2+0.5, point_x)
                            glVertex3f(normal[j][i][1]*2+2.5, normal[j]
                                       [i][0]*2+0.5,  point_xbis)
                            # calcul
                        else:

                            point_xbis = point_x + (-1)*pente_xbis
                            glVertex3f(normal[j][i][1]*2+1.5,
                                       normal[j][i][0]*2+0.5, point_x)
                            glVertex3f(normal[j][i][1]*2+0.5,
                                       normal[j][i][0]*2+0.5,  point_xbis)

                    pente_y = matrice_map[j+1, i]-matrice_map[j, i]
                    point_y = matrice_map[j, i]+(pente_y/2)
                    # POLY PENTE y
                    if point_y == matrice_map[j, i]:
                        # if c'est plat
                        glVertex3f(normal[j][i][1]*2+0.5,
                                   normal[j][i][0]*2+1.5, point_y)
                        glVertex3f(normal[j][i][1]*2+0.5,
                                   normal[j][i][0]*2+1.5,  point_y+3)
                    else:

                        pente_ybis = -1/pente_y
                        # si la pente monte
                        if pente_y < 0:

                            point_ybis = point_y+pente_ybis

                            glVertex3f(normal[j][i][1]*2+0.5,
                                       normal[j][i][0]*2+1.5, point_y)
                            glVertex3f(normal[j][i][1]*2+0.5,
                                       normal[j][i][0]*2+2.5,  point_ybis)
                        else:
                            point_ybis = point_y + (-1)*pente_ybis
                            glVertex3f(normal[j][i][1]*2+0.5,
                                       normal[j][i][0]*2+1.5, point_y)
                            glVertex3f(normal[j][i][1]*2+0.5,
                                       normal[j][i][0]*2+0.5,  point_ybis)

        glEnd()
    #  animation
    if anim == True:
        animation(cpt_x, cpt_y, matrice_map)

    else:

        cpt_x = depart_open[0]
        cpt_y = depart_open[1]
        animation(cpt_x, cpt_y, matrice_map)

    glPopMatrix()

    glutSwapBuffers()

    glLoadIdentity()

    gluLookAt(*eye, *center, *up_vec)
    glRotatef(eye_angle_y, 0.0, 1.0, 0.0)
    glRotatef(eye_angle_x, 1.0, 0, 0)
    glRotatef(eye_angle_z, 0, 0, 1.0)
    anim_bouton = False


def bary_bezier_opengl(x0, y0, x1, y1, x2, y2, x3, y3, t):
    """
    Calcule les barycentres des 4 points de controles
    avec un coefficient t
    """
    # Generation 1
    x0i = (1 - t) * x0 + x1 * t
    y0i = (1 - t) * y0 + y1 * t
    x1i = (1 - t) * x1 + x2 * t
    y1i = (1 - t) * y1 + y2 * t
    x2i = (1 - t) * x2 + x3 * t
    y2i = (1 - t) * y2 + y3 * t

    x0, y0, x1, y1, x2, y2 = x0i, y0i, x1i, y1i, x2i, y2i

    # Generation 2
    x0i = (1 - t) * x0 + x1 * t
    y0i = (1 - t) * y0 + y1 * t
    x1i = (1 - t) * x1 + x2 * t
    y1i = (1 - t) * y1 + y2 * t

    x0, y0, x1, y1 = x0i, y0i, x1i, y1i

    # Generation 3
    x0i = (1 - t) * x0 + x1 * t
    y0i = (1 - t) * y0 + y1 * t

    return x0i, y0i


def trace_beizier_quatre_opengl(x0, y0, x1, y1, x2, y2, x3, y3, it, debut=0):
    """
    Calcule les barycentres de 4 points avec un nombre d'itérations
    la variable debut definit l'endroit où la courbe commence s'afficher
     exemple 0.25 on commence au 2ème point de controle
    """
    global matrice_map, cpt_x, cpt_y, center, up_vec
    u = debut

    pas = 1/100

    #xi, yi = bary_bezier(x0,y0,x1,y1,x2,y2,x3,y3,u)
    while (u <= 1):
        xi, yi = bary_bezier_opengl(x0, y0, x1, y1, x2, y2, x3, y3, u)

        sleep(0.01)
        cpt_x = xi
        cpt_y = yi
        # position regarde
        center[0] = cpt_x*2

        center[2] = cpt_y*2

        eye[2] = 20+cpt_x
        eye[0] = 10+cpt_y
        eye[1] = 10
        print("eye", eye)
        display()

        u += pas


def trace_beizier_opengl(liste_points, it):
    """
    Trace une coube de bézier sur OpenGL, prend en paramètre
    une liste de points
    """

    n = len(liste_points)
    if(n < 4):
        print("Pas assez de points")
        return -1

    #mobile_2D = Chenille_2D(*liste_points[0], 7, Canva, cote)
    n_hors = (n - 4) % 3  # n_hors donne le nombre de points qui ne sont
    # pas dans un quadruplet

    n_int = n-n_hors-1
    # On trace la courbe pour le cas général
    # for i in range(0, n_int, 3):
    i = 0
    while(i < n_int):
        trace_beizier_quatre_opengl(*liste_points[i], *liste_points[i+1],
                                    *liste_points[i+2], *liste_points[i+3], it)
        i += 3

    # On vérifie que l'on ne se trouve pas dans le cas particulier où
    # il n'y que 4 points dans la liste
    if(n != 4):

        # Il y a 2 points hors des quadruplets
        if n_hors == 2:
            trace_beizier_quatre_opengl(*liste_points[-4], *liste_points[-3],
                                        *liste_points[-2], *liste_points[-1],
                                        it, 0.25)

        # Il y a 1 point hors des quadruplets
        elif n_hors == 1:
            trace_beizier_quatre_opengl(*liste_points[-4], *liste_points[-3],
                                        *liste_points[-2], *liste_points[-1],
                                        it, 0.75)
        # Trace sur OpenGL le dernier point de la courbe


def reshape(width, height):

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width/height, 1, 1000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(*eye, *center, *up_vec)


def keyboard(key, x, y):
    global DISPLAY_GRID, eye_angle_x, eye_angle_y, eye_angle_z, center, up_vec
    global pos, anim, anim_bouton
    global cpt_translate, normals
    global chemin
    # Zoom deplacement de la cam era selon l'axe z
    if key == b'z':
        eye[2] -= 1
        anim_bouton = True
    elif key == b's':
        eye[2] += 1
        anim_bouton = True
    # #deplacement de la camera selon l'axe y
    elif key == b'q':
        cpt_translate += 1
        glTranslated(0, cpt_translate, 0)
        anim_bouton = True
    elif key == b'd':
        cpt_translate -= 1
        glTranslated(0, cpt_translate, 0)
        anim_bouton = True
    # deplacement de la camera selon l'axe x
    elif key == b'w':
        anim_bouton = True
        eye[0] += 1
    elif key == b'x':
        eye[0] -= 1
        anim_bouton = True
    # Deplacement du centre sur l'axe x
    elif key == b'f':
        center[0] -= 1
        anim_bouton = True
    elif key == b'h':
        center[0] += 1
        anim_bouton = True
    # Rotation sur l'axe z
    elif key == b'Q':

        eye_angle_z = (eye_angle_z + 5) % 360
        anim_bouton = True
    elif key == b'D':
        eye_angle_z = (eye_angle_z - 5) % 360
        anim_bouton = True
    # Rotation sur l'axe y
    elif key == b'Z':
        eye_angle_y = (eye_angle_y + 5) % 360
        anim_bouton = True
    elif key == b'S':
        eye_angle_y = (eye_angle_y - 5) % 360
        anim_bouton = True

    # Rotation sur l'axe x
    elif key == b'W':
        eye_angle_x = (eye_angle_x + 5) % 360
        anim_bouton = True
    elif key == b'X':
        eye_angle_x = (eye_angle_x - 5) % 360

        anim_bouton = True
    elif key == b'a':
        anim = True
        it = 100
        trace_beizier_opengl(chemin, it)
    elif key in (b'n', b'N'):
        normals = 1 - normals
    elif key == b'\033':
        glutDestroyWindow(WIN)
        sys.exit(0)
    print(eye_angle_x, eye_angle_y, eye_angle_z)
    glutPostRedisplay()  # indispensable en Python


###############################################################
# MAIN

def opengl(matrice, depart, arrivee, trajet):
    global matrice_map, depart_open, arrivee_open, chemin
    matrice_map = matrice
    depart_open = depart

    arrivee_open = arrivee
    chemin = trajet
    # initialization GLUT library
    glutInit()
    # initialization display mode RGBA mode and double buffered window
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA | GLUT_DEPTH)

    # creation of top-level window
    WIN2 = glutCreateWindow('projet')

    glutReshapeWindow(800, 800)

    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)

    init()
    glutMainLoop()
