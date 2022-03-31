#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

###############################################################
# portage de planet.c
from map import *

###############################################################
# Variables Globales

#postitionement
x_pos, y_pos, z_pos = 0, 0, 5

eye_angle_x, eye_angle_y, eye_angle_z = 0, 0, 0
eye = [0, 0, 10]
center = [0,0,0]
up_vec = [1,1,0]

#Couleurs
diffuse = [0.7, 0.7, 0.7, 1.0]
specular = [0.001, 0.001, 0.001, 1.0]
pos = [1, 1, 1, 0]

quadric = None
DISPLAY_GRID = False
############################################################## #

matrice_map = generation_matrice(30)
matrice_map = tukey(matrice_map, 2)

def init():
    global quadric
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

    glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glPushMatrix()

    #Modelisation du repere othonorme
    #centre
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [1, 1, 1, 1.0])
    gluSphere(quadric, 0.2, 20, 16)

    #Axe z Bleu
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0, 0, 1, 1.0])
    gluCylinder(quadric, 0.1, 0.1, 1000, 20, 16);

    #Axe y Vert
    glPushMatrix()
    glRotatef(90, 0, 1, 0)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0, 1, 0, 1.0])
    gluCylinder(quadric, 0.1, 0.1, 1000, 20, 16);
    glPopMatrix()

    #Axe x Rouge
    glPushMatrix()
    glRotatef(90, 1, 0, 0)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [1, 0, 0, 1.0])
    gluCylinder(quadric, 0.1, 0.1, 1000, 20, 16);
    glPopMatrix()

    grid_map(matrice_map)
    glPopMatrix()

    glutSwapBuffers()
    glutSwapBuffers()
    glLoadIdentity()

    gluLookAt(*eye,*center,*up_vec)
    glRotatef(eye_angle_y, 0.0, 1.0, 0.0)
    glRotatef(eye_angle_x, 1.0, 0, 0)
    glRotatef(eye_angle_z, 0, 0, 1.0)

def reshape(width, height):

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width/height, 1, 500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(*eye,*center,*up_vec)

def keyboard(key, x, y):
    global DISPLAY_GRID, eye_angle_x, eye_angle_y, eye_angle_z, center,up_vec

    if key == b'g':
            DISPLAY_GRID = not DISPLAY_GRID

    #Zoom deplacement de la camera selon l'axe z
    elif key == b'z':
        eye[2]-=1

    elif key == b's':
         eye[2]+=1
    # #deplacement de la camera selon l'axe y
    # elif key == b'8':
    #     eye[1]+=1
    # elif key == b'2':
    #     eye[1]-=1
    # #deplacement de la camera selon l'axe x
    # elif key == b'4':
    #     eye[0]+=1
    # elif key == b'6':
    #     eye[0]-=1

    #Deplacement du centre sur l'axe x
    elif key == b'q':
        center[0]-=1

    elif key == b'd':
        center[0]+=1

    #Rotation sur l'axe z
    elif key == b'9':
        eye_angle_z = (eye_angle_z + 5) % 360

    elif key == b'3':
        eye_angle_z = (eye_angle_z - 5) % 360


    #Rotation sur l'axe y
    elif key == b'Z':
        eye_angle_y = (eye_angle_y + 5) % 360

    elif key == b'S':
        eye_angle_y = (eye_angle_y - 5) % 360

    #Rotation sur l'axe x
    elif key == b'Q':
        eye_angle_x = (eye_angle_x + 5) % 360

    elif key == b'D':
        eye_angle_x = (eye_angle_x - 5) % 360
# faire transaltion

    elif key == b'\033':
        glutDestroyWindow(WIN)
        sys.exit(0)
    glutPostRedisplay()  # indispensable en Python
    print(eye)


###############################################################
# MAIN

if __name__ == "__main__":
    # initialization GLUT library
    glutInit()
    # initialization display mode RGBA mode and double buffered window
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA |GLUT_DEPTH )

    # creation of top-level window
    WIN = glutCreateWindow('projet')

    glutReshapeWindow(800,800)

    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)

    init()

    glutMainLoop()
