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


def vec_2D(xi: float, yi: float, xj: float, yj: float):
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


def hex_to_rgb(value: str) -> tuple:
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_hex(red: int, green: int, blue: int):
    """Return color as #rrggbb for the given color values."""
    return '#%02x%02x%02x' % (red, green, blue)


def shade_color(color: tuple, factor: float) -> list:
    """
    Retourne la couleur rgb assombri ou éclaircir
    """
    shaded_color = []
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
    if((denominateur := max_value - min_value) == 0):
        denominateur = min_value
    return (valeur-min_value)/(denominateur)


def get_color(val: float) -> str:
    """
    Récupère la couleur en niveau de gris
    pour une intensité donnée
    """
    if val == np.inf or val == np.NaN:
        color = (50, 50, 255)
    else:
        norm = normalisation(val)
        color = shade_color((255, 255, 255), 1-norm)
    return rgb_to_hex(*color)


def get_color_rgb(val: float) -> str:
    """
    Récupère la couleur en niveau de gris
    pour une intensité donnée
    """
    if val == np.inf or val == np.NaN:
        color = (50, 50, 255)
    else:
        norm = normalisation(val)
        color = shade_color((255, 255, 255), 1-norm)
    return color


def green_to_brown_gradient_maping(val: float):
    """
    Prend entrée une valeur entre 0 et 1
    et renvoie selon son intensité une couleur
    entre le vert et le marron
    """
    val = normalisation(val)
    rgb = [f_r(val), f_g(val), f_b(val)]
    i = 0
    # Si la valeur 255 ou 0 est dépassé
    while i < 3:
        if(rgb[i] > 255):
            rgb[i] = 255
        if(rgb[i] < 0):
            rgb[i] = 0
        i += 1

    return rgb_to_hex(*rgb)


def green_to_brown_gradient_maping_rgb(val: float):
    """
    Prend entrée une valeur entre 0 et 1
    et renvoie selon son intensité une couleur
    entre le vert et le marron
    """
    val = normalisation(val)
    rgb = [f_r(val), f_g(val), f_b(val)]
    i = 0
    # Si la valeur 255 ou 0 est dépassé
    while i < 3:
        if(rgb[i] > 255):
            rgb[i] = 255
        if(rgb[i] < 0):
            rgb[i] = 0
        i += 1
    return rgb

# Ces fonctions ont été trouvé par approximation d'un tracé
# de courbe sur 40 valeurs avec x variant de 0 à 1
# y valeur rgb variant du vert au marron


def f_r(x: float) -> int:
    return int(-109.992*x*x+184.479*x+106.805)


def f_g(x: float) -> int:
    return int(19.7949*x*x-62.9947*x+171.313)


def f_b(x: float) -> int:
    return int(34.8157*x*x-54.7612*x+10.5841)


def circle_to_oval(x: int, y: int, r: int):
    """Permet la construction d'un cercle à partir
    en utilisant la construction d'un ovale"""
    return (x-r, y-r, x+r, y+r)
