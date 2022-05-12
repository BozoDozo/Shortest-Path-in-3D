from utils import circle_to_oval
from collections import deque
from tkinter import Canvas
from math import sqrt
# def _init_boule(i: int, j: int, fact: float, index: int, chenille_id: list):
#         """
#         Initialise une des boules de la chenille sur tkinter
#         """
#         self.cote = self.cote * fact
#         xy_xy = circle_to_oval(i*self.cote+self.cote/2, j*self.cote*+self.cote/2, 0.125*self.cote)
#         chenille_id[index] = (Canva.create_oval(*xy_xy, fill="Green", state="normal", tags="chenille"))
def distance(xi,yi, xi_1, yi_1)
class Chenille_2D:
    def __init__(self, x0: int, y0: int, size:int, canva: Canvas, cote: int) -> None:
        self.size = size
        if size <= 0:
            raise ValueError("Chenille trop petite")
        self.Canva = canva
        if canva is None:
            raise ValueError("Canvas non initialisé")
        self.cote = cote
        if cote is None:
            raise ValueError("taille des carrés non initialisée")
        self.chenille_id =[]
        self.dxy = []
        self.flux = deque()
        for i in range(self.size):
            xy_xy = circle_to_oval(x0*self.cote+self.cote/2, y0*self.cote+self.cote/2, 0.125*self.cote)
            self.chenille_id.append((self.Canva.create_oval(*xy_xy, fill="Green", state="normal", tags="chenille")))
            self.dxy.append(None)
        self.Canva.update()

    def influx(self, xi:int, yi:int):
        """Gère le flux de points dans l'environement 2D"""
        if(len(self.flux) > self.size):
            self.flux.popleft()
        self.flux.append((xi,yi))
        
    def distances(self):
        """
        Calcule les déplacements relatifs entre tous les points dans
        le flux
        """
        for idx in range(1, len(self.flux), 1):
            neg_idx = -idx
            dx = self.flux[neg_idx][0] - self.flux[neg_idx-1][0]
            dy = self.flux[neg_idx][1] - self.flux[neg_idx-1][1]
            self.dxy[neg_idx] = dx,dy

    def move(self):
        """
        Gère le déplacement des boules
        """
        self.distances()
        idx = -1
        while(idx > (-self.size)-1) and(self.dxy[idx] is not None):
            dx, dy = self.dxy[idx]
            dx, dy = dx*self.cote, dy*self.cote
            self.Canva.move(self.chenille_id[idx],dx,dy)
            #self.Canva.update()
            idx-=1
        self.Canva.update()
    
    def delete(self):
        self.Canva.delete("chenille")

    

    


