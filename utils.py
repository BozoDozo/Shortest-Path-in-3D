import numpy as np
from math import sqrt
# Variables globale
min_value = None
max_value = None
mat = None

def distance_eucl(x0: float, y0: float, x1: float, y1: float):
    """
    Calcule la distance euclidienne entre 2 points
    """
    return sqrt((x1-x0)*(x1-x0)+(y1-y0)*(y1-y0))


def vec_2D(xi:float, yi:float, xj:float, yj:float):
    """
    Calcule le vecteur i,j
    """
    return xj-xi, yj-yi
    
def get_info_matrice(min: float, max: float, matrice: np.matrix):
    """
    Récupère les informations de la matrice
    """
    global min_value, max_value, mat
    min_value, max_value, mat = min, max, matrice

def hex_to_rgb(value: str)-> tuple:
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb_to_hex(red: int, green: int, blue: int):
    """Return color as #rrggbb for the given color values."""
    return '#%02x%02x%02x' % (red, green, blue)

def shade_color(color: tuple, factor:float) -> list:
        """
        Retourne la couleur rgb assombri ou éclaircir
        """
        shaded_color= []
        for c in color:
            x = int(c * factor)
            if(x > 255):
                x = 255
            if(x < 0):
                x = 0
            shaded_color.append(x)
        return shaded_color


def normalisation(valeur: float) -> float:
    """
    Normalise d'une valeur en fonction du minimum et du maximum dans une matrice
    """
    if( (denominateur := max_value - min_value) == 0):
        denominateur = min_value
    return (valeur-min_value)/(denominateur)

def get_color(val: float) -> str:
    """
    Récupère la couleur en niveau de gris
    pour une intensité donnée
    """
    if val == np.inf or val == np.NaN:
        color = (50,50,255)
    else:
        norm = normalisation(val)
        color = shade_color((255, 255, 255), 1-norm)
    return rgb_to_hex(*color)

def circle_to_oval(x: int, y: int, r: int):
    """Permet la construction d'un cercle à partir
    en utilisant la construction d'un ovale"""
    return (x-r, y-r, x+r, y+r)