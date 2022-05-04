import tkinter as tk
from tkinter import filedialog
from save import lire_matrice
from map import generation_matrice_terrain
# Variable Gloables
Matrice = [[float('inf'), 3, 5, 5, 8, 6, 7, 3, 3, float('inf')],
           [4, 5, 5, 5, 6, 6, 7, 3, 3, float('inf')],
           [5, 4, 4, 4, 6, 7, 8, 7, 3, float('inf')],
           [6, 5, 5, 4, 3, 6, 9, 8, 7, 7],
           [7, 7, 7, 6, 6, 6, 7, 8, 7, 7],
           [6, 7, 7, 7, 7, 5, 7, 4, 3, float('inf')],
           [8, 7, 8, 7, 7, 6, 6, float('inf'), float('inf'), float('inf')],
           [4, 5, 5, 8, 8, 6, 6, 6, 4, float('inf')],
           [3, 5, 5, 6, 6, 6, 6, 5, 4, float('inf')],
           [float('inf'), 4, 4, 5, 5, 6, 6, 6, 5, 3]]


# Fonction pour les boutons

def ouvrir_fichier():
    """
    Renvoie le chemin du fichier sélectionné
    """
    return filedialog.askopenfilename()


def ouvrir_matrice():
    """
    Ouvre une matrice
    """
    global Matrice
    if((path := ouvrir_fichier()) != ""):
        Matrice = lire_matrice(path)


def generation_matrice():
    """
    Génère une nouvelle matrice à l'écran avec
    les paramètres demandés en ihm
    """
    global Matrice
    n = 10
    borne = 10
    flat = 1
    obs = False
    cran = 0
    win_2 = tk.Toplevel(win)
    win_2.title("Generation de Matrice")
    scale_matrice = tk.Scale(win_2, label="Taille de la matrice", from_=5, to_=50, variable=n , orient="horizontal").pack(side="top")
    scale_borne = tk.Scale(win_2, label="Borne supérieur des valeurs", from_=2, to_=100, variable=borne, orient="horizontal").pack(side="top")
    scale_flatness = tk.Scale(win_2, label="Taux d’aplatissement des valeurs", from_=0, to_=10, variable=flat, orient="horizontal").pack(side="top")
    scale_obstacle = tk.Checkbutton(win_2, text= "Présence d'obstacles", variable=obs).pack(side="top")
    scale_cran_obstacle = tk.Scale(win_2, label="Taux d’obstacles", from_=0, to_=100, variable=cran, orient="horizontal").pack(side="top")
    bouton_confirmer = tk.Button(win_2,text="Valider",command=lambda:nouvelle_matrice(win_2, n, borne, flat, obs, cran)).pack(side="bottom")
    print(n, borne, flat, obs, cran)

def nouvelle_matrice(win: tk.Toplevel, taille : int, borne_sup: int, flatness: int, a_obstacle: int, cran_obstacle: int):
    global Matrice
    Matrice = generation_matrice_terrain(taille, 1, borne_sup, flatness, a_obstacle, cran_obstacle )
    print(Matrice)
    print(taille,  borne_sup, flatness,a_obstacle, cran_obstacle)
    win.destroy()



# Initialisation des fenêtres

win = tk.Tk()
win.title("Plan du terrain")


top_frame = tk.Frame(win)
# fichier_button = tk.Menubutton(top_frame, text="Fichier")
# menu_fichier = tk.Menu(fichier_button,tearoff=False)
# menu_fichier.add_command(label="Ouvrir Matrice")
# menu_fichier.add_separator()
# menu_fichier.add_command(label="Sauver Matrice")
# menu_fichier.add_separator()
# menu_fichier.add_command(label="Nouvelle Matrice")
# menu_fichier.add_separator()
# menu_fichier.add_command(label="Quitter")
# fichier_button.config(menu=menu_fichier)
charger_matrice = tk.Button(
    top_frame, text="Ouvrir Matrice", width=20, command=ouvrir_matrice)
generer_matrice = tk.Button(
top_frame, text="Générer Matrice", width=20, command=generation_matrice)
aide = tk.Button(top_frame, text="Aide", width=20)
canva = tk.Canvas(win, height=700, width=600)


# Disposition des Widgets
# Disposition des Widgets
charger_matrice.pack(side="left")
generer_matrice.pack(side="left")
aide.pack(side="right")
top_frame.pack(side="top", fill=tk.X)
# fichier_button.pack(side ="left")
# aide_button.pack(side="right")
canva.pack(side="top")


tk.mainloop()

exit(0)
