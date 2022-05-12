from utils import circle_to_oval
from collections import deque
from tkinter import Canvas
from math import sqrt
from utils import distance_eucl, vec_2D
# def _init_boule(i: int, j: int, fact: float, index: int, chenille_id: list):
#         """
#         Initialise une des boules de la chenille sur tkinter
#         """
#         self.cote = self.cote * fact
#         xy_xy = circle_to_oval(i*self.cote+self.cote/2, j*self.cote*+self.cote/2, 0.125*self.cote)
#         chenille_id[index] = (Canva.create_oval(*xy_xy, fill="Green", state="normal", tags="chenille"))


def pos_suiv(xi:float, yi: float, xj_1: float, yj_1: float, dist:float):
    """ Calcul de la position des boules"""
    # Comme la distance est une constante on la passe
    # directement en parametre
    # On normalise le vecteur unitaire
    u = vec_2D(xi, yi, xj_1, yj_1)
    norm = distance_eucl(xi, yi, xj_1, yj_1)
    # On applique la distance constante
    u = dist*u[0]/norm,  dist*u[1]/norm
    # On soustrait pour obtenir la bonne position
    return xj_1-u[0], yj_1-u[1]



class Chenille_2D:
    def __init__(self, x0: float, y0: float, size:int, canva: Canvas, cote: int) -> None:
        self.size = size
        # Nombre de boules
        if size <= 0:
            raise ValueError("Chenille trop petite")
        # Canvas
        self.Canva = canva
        if canva is None:
            raise ValueError("Canvas non initialisé")
        # Taille du carre dans le canvas
        self.cote = cote
        if cote is None:
            raise ValueError("taille des carrés non initialisée")
        # Tableau pour stocker l'id des boules
        self.chenille_id =[]
        # Tableau des disntaces
        self.dxy = []
        # File pour récupérer les point des bézier courants
        self.flux = deque()
        # Distance constantes entre chaque boules
        self.dcst = []
        self.pos = []
        # Position des boules
        # Initialisation des boules
        x0, y0 = x0-2, y0-2
        for i in range(self.size):
            fact = 1+i*0.05
            dist = 1*i*0.05
            xy_xy = circle_to_oval(x0*self.cote+self.cote/2, y0*self.cote+self.cote/2, fact*0.175*self.cote)
            self.chenille_id.append((self.Canva.create_oval(*xy_xy, fill="Green", state="normal", tags="chenille")))
            self.pos.append((x0, y0))
            self.dxy.append(None)
            self.dcst.append(dist)
        self.Canva.update()

    def influx(self, xi:int, yi:int):
        """Gère le flux de points dans l'environement 2D"""
        if(len(self.flux) > 2):
            self.flux.popleft()
        self.flux.append((xi,yi))
        
    def deplacement(self, xj_1: float, yj_1: float):
        """
        Calcule les déplacements relatifs entre tous les points dans
        le flux
        """
        # Déplacement de la tête
        # Calcul du vecteur tête
        print(self.pos[-1])
        print(xj_1, yj_1)
        dx, dy = xj_1-self.pos[-1][0], yj_1-self.pos[-1][1]
        # On multiplie par la taille des carres pour avoir les bons repères
        self.Canva.move(self.chenille_id[-1],dx *self.cote, dy*self.cote)
        self.pos[-1] = xj_1, yj_1
        print(self.pos[-1])
        idx = -2
        while(idx > (-self.size)-1):
            # On récupère la position de la prochaine boule
            xj_1, yj_1 = self.pos[idx+1]
            xi, yi = self.pos[idx]
            cste = self.dcst[idx]
            # On calcule la position de la prochaine boule
            xj, yj = pos_suiv(xi, yi, xj_1, yj_1, cste)
            self.pos[idx] = xj, yj
            dx, dy = xj-xi, yj-yi
            self.Canva.move(self.chenille_id[idx], dx *self.cote, dy*self.cote)
            
            #
            idx -= 1

    def delete(self):
        self.Canva.delete("chenille")

    

    


